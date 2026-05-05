(function () {
    'use strict';

    const STORAGE_KEY = 'fitnessTracker.v1';

    const defaultState = {
        settings: {
            startWeight: 0,
            targetLoss: 10,
            targetDate: '2026-07-01',
            units: 'lb',
        },
        weights: [],   // [{ id, date: 'YYYY-MM-DD', value: number }]
        workouts: [],  // [{ id, date, category, exercise, sets, reps, weight, notes }]
    };

    // ---------- Storage ----------
    function load() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return structuredClone(defaultState);
            const parsed = JSON.parse(raw);
            return {
                settings: { ...defaultState.settings, ...(parsed.settings || {}) },
                weights: Array.isArray(parsed.weights) ? parsed.weights : [],
                workouts: Array.isArray(parsed.workouts) ? parsed.workouts : [],
            };
        } catch (e) {
            console.error('Failed to load state', e);
            return structuredClone(defaultState);
        }
    }

    function save() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    let state = load();

    // ---------- Helpers ----------
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    function todayISO() {
        const d = new Date();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${d.getFullYear()}-${m}-${day}`;
    }

    function uid() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
    }

    function fmtWeight(n) {
        if (n == null || isNaN(n)) return '—';
        return Number(n).toFixed(1);
    }

    function fmtDate(iso) {
        const [y, m, d] = iso.split('-').map(Number);
        const dt = new Date(y, m - 1, d);
        return dt.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    }

    function daysBetween(isoA, isoB) {
        const a = new Date(isoA + 'T00:00:00');
        const b = new Date(isoB + 'T00:00:00');
        return Math.round((b - a) / 86400000);
    }

    function sortedWeights() {
        return [...state.weights].sort((a, b) => a.date.localeCompare(b.date));
    }

    // ---------- Tabs ----------
    function initTabs() {
        $$('.tab').forEach((tab) => {
            tab.addEventListener('click', () => {
                $$('.tab').forEach((t) => t.classList.remove('active'));
                $$('.tab-panel').forEach((p) => p.classList.remove('active'));
                tab.classList.add('active');
                $('#tab-' + tab.dataset.tab).classList.add('active');
            });
        });
    }

    // ---------- Goal panel ----------
    function renderGoal() {
        const { settings } = state;
        const sorted = sortedWeights();
        const latest = sorted[sorted.length - 1];
        const current = latest ? latest.value : settings.startWeight;
        const target = settings.startWeight - settings.targetLoss;
        const toGo = current - target;
        const daysLeft = settings.targetDate ? daysBetween(todayISO(), settings.targetDate) : 0;

        $('#stat-current').textContent = settings.startWeight ? fmtWeight(current) : '—';
        $('#stat-target').textContent = settings.startWeight ? fmtWeight(target) : '—';
        $('#stat-togo').textContent = settings.startWeight ? fmtWeight(Math.max(0, toGo)) : '—';
        $('#stat-days').textContent = daysLeft >= 0 ? daysLeft : 0;

        $('#stat-current-unit').textContent = settings.units;
        $('#stat-target-unit').textContent = settings.units;
        $('#stat-togo-unit').textContent = settings.units;

        // Progress: how much of targetLoss has been achieved
        const lost = Math.max(0, settings.startWeight - current);
        const pct = settings.targetLoss > 0
            ? Math.min(100, Math.max(0, (lost / settings.targetLoss) * 100))
            : 0;
        $('#progress-fill').style.width = pct.toFixed(1) + '%';
        $('#progress-pct').textContent = pct.toFixed(0) + '% there';

        const note = $('#goal-note');
        note.classList.remove('on-track', 'behind', 'far-behind');

        if (!settings.startWeight) {
            $('#progress-pace').textContent = '—';
            note.textContent = 'Set your starting weight in Settings to get started.';
            return;
        }

        if (daysLeft <= 0) {
            $('#progress-pace').textContent = 'Target date reached';
            if (toGo <= 0) {
                note.textContent = `You hit your goal! Final: ${fmtWeight(current)} ${settings.units}.`;
                note.classList.add('on-track');
            } else {
                note.textContent = `Target date passed. ${fmtWeight(toGo)} ${settings.units} short — set a new goal in Settings.`;
                note.classList.add('behind');
            }
            return;
        }

        if (toGo <= 0) {
            $('#progress-pace').textContent = 'Goal reached';
            note.textContent = `You hit your goal with ${daysLeft} day${daysLeft === 1 ? '' : 's'} to spare!`;
            note.classList.add('on-track');
            return;
        }

        const lbsPerWeek = (toGo / daysLeft) * 7;
        $('#progress-pace').textContent = `${lbsPerWeek.toFixed(2)} ${settings.units}/wk needed`;

        // Pace assessment
        if (sorted.length >= 2) {
            const first = sorted[0];
            const elapsedDays = Math.max(1, daysBetween(first.date, latest.date));
            const actualPerWeek = ((first.value - latest.value) / elapsedDays) * 7;
            if (actualPerWeek >= lbsPerWeek * 0.9) {
                note.textContent = `On track — losing ~${actualPerWeek.toFixed(2)} ${settings.units}/wk, need ${lbsPerWeek.toFixed(2)}.`;
                note.classList.add('on-track');
            } else if (actualPerWeek > 0) {
                note.textContent = `A bit behind — losing ~${actualPerWeek.toFixed(2)} ${settings.units}/wk, need ${lbsPerWeek.toFixed(2)}.`;
                note.classList.add('behind');
            } else {
                note.textContent = `Off pace — weight is flat or up. Need ${lbsPerWeek.toFixed(2)} ${settings.units}/wk to hit goal.`;
                note.classList.add('far-behind');
            }
        } else {
            note.textContent = `Need ${lbsPerWeek.toFixed(2)} ${settings.units}/wk over ${daysLeft} days. Log entries to track pace.`;
        }
    }

    function renderStreak() {
        const today = todayISO();
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        const isoSeven = sevenDaysAgo.toISOString().slice(0, 10);
        const isoThirty = thirtyDaysAgo.toISOString().slice(0, 10);

        const week = new Set();
        const month = new Set();
        let monthVolume = 0;

        state.workouts.forEach((w) => {
            if (w.date >= isoSeven && w.date <= today) week.add(w.date);
            if (w.date >= isoThirty && w.date <= today) {
                month.add(w.date);
                const wt = Number(w.weight) || 0;
                const reps = (Number(w.sets) || 0) * (Number(w.reps) || 0);
                monthVolume += wt > 0 ? wt * reps : reps; // bodyweight: count reps
            }
        });

        $('#stat-week-workouts').textContent = week.size;
        $('#stat-month-workouts').textContent = month.size;
        $('#stat-month-volume').textContent = Math.round(monthVolume).toLocaleString();
        $('#stat-volume-unit').textContent = `${state.settings.units}·reps`;
    }

    // ---------- Weight panel ----------
    function initWeightForm() {
        $('#weight-date').value = todayISO();
        $('#weight-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const date = $('#weight-date').value;
            const value = parseFloat($('#weight-value').value);
            if (!date || isNaN(value) || value <= 0) return;

            // Replace same-day entry instead of duplicating
            state.weights = state.weights.filter((w) => w.date !== date);
            state.weights.push({ id: uid(), date, value });
            save();
            $('#weight-value').value = '';
            renderAll();
        });
    }

    function renderWeightTable() {
        const tbody = $('#weight-table tbody');
        tbody.innerHTML = '';
        const sorted = sortedWeights();
        const empty = $('#weight-empty');
        const table = $('#weight-table');

        if (sorted.length === 0) {
            empty.classList.remove('hidden');
            table.style.display = 'none';
            return;
        }
        empty.classList.add('hidden');
        table.style.display = '';

        // Show newest first
        const reversed = [...sorted].reverse();
        reversed.forEach((entry, i) => {
            const prev = reversed[i + 1]; // older one
            const change = prev ? entry.value - prev.value : null;
            const tr = document.createElement('tr');

            const tdDate = document.createElement('td');
            tdDate.textContent = fmtDate(entry.date);
            tr.appendChild(tdDate);

            const tdVal = document.createElement('td');
            tdVal.textContent = `${fmtWeight(entry.value)} ${state.settings.units}`;
            tr.appendChild(tdVal);

            const tdChg = document.createElement('td');
            if (change == null) {
                tdChg.textContent = '—';
                tdChg.className = 'change-flat';
            } else if (change < 0) {
                tdChg.textContent = `↓ ${fmtWeight(Math.abs(change))}`;
                tdChg.className = 'change-down';
            } else if (change > 0) {
                tdChg.textContent = `↑ ${fmtWeight(change)}`;
                tdChg.className = 'change-up';
            } else {
                tdChg.textContent = '—';
                tdChg.className = 'change-flat';
            }
            tr.appendChild(tdChg);

            const tdAct = document.createElement('td');
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-icon';
            btn.textContent = '✕';
            btn.title = 'Delete entry';
            btn.addEventListener('click', () => {
                state.weights = state.weights.filter((w) => w.id !== entry.id);
                save();
                renderAll();
            });
            tdAct.appendChild(btn);
            tr.appendChild(tdAct);

            tbody.appendChild(tr);
        });
    }

    function renderChart() {
        const svg = $('#weight-chart');
        const empty = $('#chart-empty');
        svg.innerHTML = '';
        const sorted = sortedWeights();

        if (sorted.length < 1) {
            empty.style.display = '';
            svg.style.display = 'none';
            return;
        }
        empty.style.display = 'none';
        svg.style.display = '';

        const W = 600, H = 220, padL = 40, padR = 12, padT = 12, padB = 28;
        const innerW = W - padL - padR;
        const innerH = H - padT - padB;

        const target = state.settings.startWeight - state.settings.targetLoss;
        const hasGoal = state.settings.startWeight > 0 && state.settings.targetLoss > 0;
        const values = sorted.map((w) => w.value);
        if (hasGoal) values.push(state.settings.startWeight, target);

        const min = Math.min(...values) - 1;
        const max = Math.max(...values) + 1;
        const range = max - min || 1;

        const startDate = sorted[0].date;
        const endDate = sorted[sorted.length - 1].date;
        const totalDays = daysBetween(startDate, endDate);

        const xFor = (iso) => {
            if (totalDays <= 0) return padL + innerW / 2;
            return padL + (daysBetween(startDate, iso) / totalDays) * innerW;
        };
        const yFor = (v) => padT + ((max - v) / range) * innerH;

        const ns = 'http://www.w3.org/2000/svg';

        // Grid lines (4 horizontal)
        for (let i = 0; i <= 4; i++) {
            const y = padT + (innerH / 4) * i;
            const val = max - (range / 4) * i;
            const line = document.createElementNS(ns, 'line');
            line.setAttribute('class', 'grid-line');
            line.setAttribute('x1', padL);
            line.setAttribute('x2', W - padR);
            line.setAttribute('y1', y);
            line.setAttribute('y2', y);
            svg.appendChild(line);

            const label = document.createElementNS(ns, 'text');
            label.setAttribute('class', 'axis-label');
            label.setAttribute('x', 4);
            label.setAttribute('y', y + 4);
            label.textContent = val.toFixed(0);
            svg.appendChild(label);
        }

        // Target line
        if (hasGoal && target >= min && target <= max) {
            const y = yFor(target);
            const line = document.createElementNS(ns, 'line');
            line.setAttribute('class', 'target-line');
            line.setAttribute('x1', padL);
            line.setAttribute('x2', W - padR);
            line.setAttribute('y1', y);
            line.setAttribute('y2', y);
            svg.appendChild(line);

            const label = document.createElementNS(ns, 'text');
            label.setAttribute('class', 'axis-label');
            label.setAttribute('x', W - padR - 50);
            label.setAttribute('y', y - 4);
            label.setAttribute('fill', '#14b8a6');
            label.textContent = `target ${target.toFixed(1)}`;
            svg.appendChild(label);
        }

        // Data line + area
        if (sorted.length >= 2) {
            const pts = sorted.map((w) => `${xFor(w.date)},${yFor(w.value)}`).join(' ');
            const polyline = document.createElementNS(ns, 'polyline');
            polyline.setAttribute('class', 'data-line');
            polyline.setAttribute('points', pts);
            svg.appendChild(polyline);

            const areaPts = `${xFor(sorted[0].date)},${padT + innerH} ${pts} ${xFor(sorted[sorted.length - 1].date)},${padT + innerH}`;
            const polygon = document.createElementNS(ns, 'polygon');
            polygon.setAttribute('class', 'data-area');
            polygon.setAttribute('points', areaPts);
            svg.appendChild(polygon);
        }

        // Data points
        sorted.forEach((w) => {
            const c = document.createElementNS(ns, 'circle');
            c.setAttribute('class', 'data-point');
            c.setAttribute('cx', xFor(w.date));
            c.setAttribute('cy', yFor(w.value));
            c.setAttribute('r', 3.5);
            const title = document.createElementNS(ns, 'title');
            title.textContent = `${fmtDate(w.date)}: ${fmtWeight(w.value)} ${state.settings.units}`;
            c.appendChild(title);
            svg.appendChild(c);
        });

        // X-axis date labels (first/last)
        const labelStart = document.createElementNS(ns, 'text');
        labelStart.setAttribute('class', 'axis-label');
        labelStart.setAttribute('x', padL);
        labelStart.setAttribute('y', H - 8);
        labelStart.textContent = fmtDate(startDate);
        svg.appendChild(labelStart);

        if (startDate !== endDate) {
            const labelEnd = document.createElementNS(ns, 'text');
            labelEnd.setAttribute('class', 'axis-label');
            labelEnd.setAttribute('x', W - padR);
            labelEnd.setAttribute('y', H - 8);
            labelEnd.setAttribute('text-anchor', 'end');
            labelEnd.textContent = fmtDate(endDate);
            svg.appendChild(labelEnd);
        }
    }

    // ---------- Workouts panel ----------
    function initWorkoutForm() {
        $('#w-date').value = todayISO();
        $('#workout-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const entry = {
                id: uid(),
                date: $('#w-date').value,
                category: $('#w-category').value,
                exercise: $('#w-exercise').value.trim(),
                sets: parseInt($('#w-sets').value, 10) || 0,
                reps: parseInt($('#w-reps').value, 10) || 0,
                weight: parseFloat($('#w-weight').value) || 0,
                notes: $('#w-notes').value.trim(),
            };
            if (!entry.date || !entry.exercise || entry.sets <= 0 || entry.reps <= 0) return;
            state.workouts.push(entry);
            save();
            $('#w-exercise').value = '';
            $('#w-notes').value = '';
            renderAll();
        });

        // Smart default for weight when category changes
        $('#w-category').addEventListener('change', (e) => {
            const cat = e.target.value;
            if (cat === 'Pushups' || cat === 'Sit-ups' || cat === 'Bodyweight') {
                $('#w-weight').value = 0;
                if (cat === 'Pushups') $('#w-exercise').value = 'Pushups';
                if (cat === 'Sit-ups') $('#w-exercise').value = 'Sit-ups';
            }
        });
    }

    function renderWorkouts() {
        const list = $('#workout-list');
        const empty = $('#workout-empty');
        list.innerHTML = '';

        if (state.workouts.length === 0) {
            empty.classList.remove('hidden');
            return;
        }
        empty.classList.add('hidden');

        // Group by date, newest first
        const byDate = {};
        state.workouts.forEach((w) => {
            (byDate[w.date] = byDate[w.date] || []).push(w);
        });
        const dates = Object.keys(byDate).sort().reverse();

        dates.forEach((date) => {
            const day = document.createElement('div');
            day.className = 'workout-day';

            const header = document.createElement('div');
            header.className = 'workout-day-header';
            const ds = document.createElement('span');
            ds.className = 'workout-day-date';
            ds.textContent = fmtDate(date);
            const meta = document.createElement('span');
            meta.className = 'workout-day-meta';
            meta.textContent = `${byDate[date].length} exercise${byDate[date].length === 1 ? '' : 's'}`;
            header.appendChild(ds);
            header.appendChild(meta);
            day.appendChild(header);

            byDate[date].forEach((w) => {
                const row = document.createElement('div');
                row.className = 'workout-entry';

                const badge = document.createElement('span');
                badge.className = 'badge';
                badge.textContent = w.category;
                row.appendChild(badge);

                const name = document.createElement('span');
                name.className = 'ex-name';
                name.textContent = w.exercise;
                row.appendChild(name);

                const detail = document.createElement('span');
                detail.className = 'ex-detail';
                const wtPart = w.weight > 0 ? ` @ ${fmtWeight(w.weight)} ${state.settings.units}` : '';
                detail.textContent = `${w.sets} × ${w.reps}${wtPart}`;
                row.appendChild(detail);

                const del = document.createElement('button');
                del.type = 'button';
                del.className = 'btn-icon';
                del.textContent = '✕';
                del.title = 'Delete';
                del.addEventListener('click', () => {
                    state.workouts = state.workouts.filter((x) => x.id !== w.id);
                    save();
                    renderAll();
                });
                row.appendChild(del);

                if (w.notes) {
                    const notes = document.createElement('div');
                    notes.className = 'ex-notes';
                    notes.textContent = w.notes;
                    row.appendChild(notes);
                }

                day.appendChild(row);
            });

            list.appendChild(day);
        });
    }

    // ---------- Settings ----------
    function loadSettingsForm() {
        $('#s-start').value = state.settings.startWeight || '';
        $('#s-loss').value = state.settings.targetLoss;
        $('#s-date').value = state.settings.targetDate;
        $('#s-units').value = state.settings.units;
    }

    function initSettings() {
        loadSettingsForm();
        $('#settings-form').addEventListener('submit', (e) => {
            e.preventDefault();
            state.settings.startWeight = parseFloat($('#s-start').value) || 0;
            state.settings.targetLoss = parseFloat($('#s-loss').value) || 0;
            state.settings.targetDate = $('#s-date').value;
            state.settings.units = $('#s-units').value;
            save();

            const flash = $('#settings-saved');
            flash.textContent = 'Saved ✓';
            flash.classList.add('show');
            setTimeout(() => flash.classList.remove('show'), 1500);

            renderAll();
        });

        $('#export-btn').addEventListener('click', () => {
            const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `fitness-tracker-${todayISO()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        });

        $('#import-input').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (ev) => {
                try {
                    const imported = JSON.parse(ev.target.result);
                    if (!imported.settings || !Array.isArray(imported.weights) || !Array.isArray(imported.workouts)) {
                        throw new Error('Invalid format');
                    }
                    state = {
                        settings: { ...defaultState.settings, ...imported.settings },
                        weights: imported.weights,
                        workouts: imported.workouts,
                    };
                    save();
                    loadSettingsForm();
                    renderAll();
                    alert('Import successful.');
                } catch (err) {
                    alert('Import failed: ' + err.message);
                }
                e.target.value = '';
            };
            reader.readAsText(file);
        });

        $('#reset-btn').addEventListener('click', () => {
            if (!confirm('Delete all weight entries, workouts, and settings? This cannot be undone.')) return;
            localStorage.removeItem(STORAGE_KEY);
            state = load();
            loadSettingsForm();
            renderAll();
        });
    }

    // ---------- Render all ----------
    function renderAll() {
        renderGoal();
        renderStreak();
        renderWeightTable();
        renderChart();
        renderWorkouts();
    }

    // ---------- Init ----------
    initTabs();
    initWeightForm();
    initWorkoutForm();
    initSettings();
    renderAll();
})();
