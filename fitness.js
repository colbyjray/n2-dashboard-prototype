(function () {
    'use strict';

    const STORAGE_KEY = 'fitnessTracker.v2';

    // ============ PROGRAM ============
    // 7-day rotation. Equipment: barbell, dumbbells, pushups, sit-ups, bodyweight only.
    // category drives the small badge; noWeight=true hides the weight input.
    const PROGRAM = [
        {
            name: 'UPPER PUSH',
            exercises: [
                { name: 'Barbell Bench Press', category: 'Barbell', sets: 4, reps: 8 },
                { name: 'Dumbbell Overhead Press', category: 'Dumbbell', sets: 3, reps: 10 },
                { name: 'Pushups', category: 'Bodyweight', sets: 3, reps: 'max', noWeight: true },
                { name: 'Dumbbell Lateral Raise', category: 'Dumbbell', sets: 3, reps: 12 },
                { name: 'Close-Grip Pushups', category: 'Bodyweight', sets: 3, reps: 'max', noWeight: true },
            ],
        },
        {
            name: 'LOWER BODY',
            exercises: [
                { name: 'Barbell Back Squat', category: 'Barbell', sets: 4, reps: 8 },
                { name: 'Barbell Romanian Deadlift', category: 'Barbell', sets: 3, reps: 10 },
                { name: 'Dumbbell Walking Lunges', category: 'Dumbbell', sets: 3, reps: '12/leg' },
                { name: 'Bodyweight Calf Raises', category: 'Bodyweight', sets: 3, reps: 20, noWeight: true },
                { name: 'Plank', category: 'Bodyweight', sets: 3, reps: '45s', noWeight: true },
            ],
        },
        {
            name: 'UPPER PULL',
            exercises: [
                { name: 'Barbell Bent-Over Row', category: 'Barbell', sets: 4, reps: 8 },
                { name: 'Dumbbell One-Arm Row', category: 'Dumbbell', sets: 3, reps: '10/side' },
                { name: 'Dumbbell Bicep Curl', category: 'Dumbbell', sets: 3, reps: 12 },
                { name: 'Dumbbell Reverse Fly', category: 'Dumbbell', sets: 3, reps: 15 },
                { name: 'Sit-ups', category: 'Sit-ups', sets: 3, reps: 20, noWeight: true },
            ],
        },
        {
            name: 'CONDITIONING',
            exercises: [
                { name: 'Burpees', category: 'Bodyweight', sets: 4, reps: 10, noWeight: true },
                { name: 'Mountain Climbers', category: 'Bodyweight', sets: 4, reps: 30, noWeight: true },
                { name: 'Jumping Jacks', category: 'Bodyweight', sets: 3, reps: 50, noWeight: true },
                { name: 'Pushups', category: 'Pushups', sets: 3, reps: 'max', noWeight: true },
                { name: 'Sit-ups', category: 'Sit-ups', sets: 3, reps: 25, noWeight: true },
            ],
        },
        {
            name: 'FULL BODY',
            exercises: [
                { name: 'Barbell Deadlift', category: 'Barbell', sets: 4, reps: 6 },
                { name: 'Dumbbell Thruster', category: 'Dumbbell', sets: 3, reps: 10 },
                { name: 'Pushups', category: 'Pushups', sets: 3, reps: 'max', noWeight: true },
                { name: 'Dumbbell Goblet Squat', category: 'Dumbbell', sets: 3, reps: 12 },
                { name: 'Sit-ups', category: 'Sit-ups', sets: 3, reps: 20, noWeight: true },
            ],
        },
        {
            name: 'CORE & CARDIO',
            exercises: [
                { name: 'Sit-ups', category: 'Sit-ups', sets: 4, reps: 25, noWeight: true },
                { name: 'Plank', category: 'Bodyweight', sets: 3, reps: '60s', noWeight: true },
                { name: 'Dumbbell Russian Twists', category: 'Dumbbell', sets: 3, reps: '30 total' },
                { name: 'Leg Raises', category: 'Bodyweight', sets: 3, reps: 15, noWeight: true },
                { name: 'Mountain Climbers', category: 'Bodyweight', sets: 3, reps: 40, noWeight: true },
                { name: 'Burpees', category: 'Bodyweight', sets: 3, reps: 10, noWeight: true },
            ],
        },
        {
            name: 'REST',
            rest: true,
            exercises: [],
        },
    ];

    const defaultState = {
        settings: {
            startWeight: 0,
            targetLoss: 10,
            targetDate: '2026-07-01',
            units: 'lb',
            programStart: null, // set on first save
        },
        weights: [],   // [{ id, date, value }]
        sessions: [],  // [{ id, date, dayIndex, dayName, isRest, completedAt, exercises:[{name,category,prescribedSets,prescribedReps,actualReps,weight,done,noWeight}] }]
    };

    // ============ STORAGE ============
    function load() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                // Migrate from v1 if present
                const v1 = localStorage.getItem('fitnessTracker.v1');
                if (v1) {
                    const parsed = JSON.parse(v1);
                    return {
                        settings: { ...defaultState.settings, ...(parsed.settings || {}) },
                        weights: Array.isArray(parsed.weights) ? parsed.weights : [],
                        sessions: [],
                    };
                }
                return structuredClone(defaultState);
            }
            const parsed = JSON.parse(raw);
            return {
                settings: { ...defaultState.settings, ...(parsed.settings || {}) },
                weights: Array.isArray(parsed.weights) ? parsed.weights : [],
                sessions: Array.isArray(parsed.sessions) ? parsed.sessions : [],
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

    // ============ HELPERS ============
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    function todayISO() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function uid() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
    }

    function fmtWeight(n) {
        if (n == null || isNaN(n)) return '—';
        return Number(n).toFixed(1);
    }

    function fmtDate(iso, opts = { month: 'short', day: 'numeric', year: 'numeric' }) {
        const [y, m, d] = iso.split('-').map(Number);
        return new Date(y, m - 1, d).toLocaleDateString(undefined, opts);
    }

    function fmtDateLong(iso) {
        const [y, m, d] = iso.split('-').map(Number);
        return new Date(y, m - 1, d).toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
    }

    function daysBetween(isoA, isoB) {
        const a = new Date(isoA + 'T00:00:00');
        const b = new Date(isoB + 'T00:00:00');
        return Math.round((b - a) / 86400000);
    }

    function sortedWeights() {
        return [...state.weights].sort((a, b) => a.date.localeCompare(b.date));
    }

    function getDayIndex(isoDate) {
        const start = state.settings.programStart || isoDate;
        const diff = daysBetween(start, isoDate);
        return ((diff % 7) + 7) % 7;
    }

    // ============ SESSIONS ============
    function getOrCreateSession(isoDate) {
        let session = state.sessions.find((s) => s.date === isoDate);
        if (session) return session;

        const idx = getDayIndex(isoDate);
        const day = PROGRAM[idx];
        session = {
            id: uid(),
            date: isoDate,
            dayIndex: idx,
            dayName: day.name,
            isRest: !!day.rest,
            completedAt: null,
            exercises: day.exercises.map((e) => ({
                name: e.name,
                category: e.category,
                prescribedSets: e.sets,
                prescribedReps: e.reps,
                actualReps: typeof e.reps === 'number' ? e.reps : null,
                weight: 0,
                noWeight: !!e.noWeight,
                done: false,
            })),
        };
        state.sessions.push(session);
        save();
        return session;
    }

    function isSessionComplete(s) {
        if (s.isRest) return s.completedAt != null;
        return s.exercises.length > 0 && s.exercises.every((e) => e.done);
    }

    function getStreak() {
        // Count consecutive days back from today where session was completed (rest days count if marked complete OR auto-pass)
        let streak = 0;
        const today = todayISO();
        let cursor = new Date(today + 'T00:00:00');

        for (let i = 0; i < 365; i++) {
            const iso = `${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, '0')}-${String(cursor.getDate()).padStart(2, '0')}`;
            const s = state.sessions.find((x) => x.date === iso);
            const idx = getDayIndex(iso);
            const isRestDay = PROGRAM[idx].rest;

            if (i === 0) {
                // Today: only count if started/finished. Don't break streak just because day isn't over.
                if (s && (isSessionComplete(s) || (isRestDay && !s.completedAt))) {
                    if (isSessionComplete(s)) streak++;
                } else if (isRestDay) {
                    // rest day not yet acknowledged — don't break, but don't count
                }
                cursor.setDate(cursor.getDate() - 1);
                continue;
            }

            if (isRestDay) {
                // Rest day: doesn't break streak even if not "done"
                cursor.setDate(cursor.getDate() - 1);
                continue;
            }

            if (s && isSessionComplete(s)) {
                streak++;
            } else {
                break;
            }
            cursor.setDate(cursor.getDate() - 1);
        }
        return streak;
    }

    // ============ TABS / NAV ============
    function initTabs() {
        $$('.nav-item').forEach((btn) => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                $$('.nav-item').forEach((b) => b.classList.remove('active'));
                $$('.tab-panel').forEach((p) => p.classList.remove('active'));
                btn.classList.add('active');
                $('#tab-' + tab).classList.add('active');
                renderAll();
                window.scrollTo(0, 0);
            });
        });
    }

    // ============ TODAY ============
    function renderToday() {
        const date = todayISO();
        const session = getOrCreateSession(date);

        $('#hero-date').textContent = fmtDateLong(date).toUpperCase();
        $('#hero-day-num').textContent = `DAY ${session.dayIndex + 1}`;
        $('#hero-title').textContent = session.dayName;

        const hero = $('#workout-hero');
        const restCard = $('#rest-card');
        const list = $('#exercise-list');
        const finishBtn = $('#finish-btn');

        if (session.isRest) {
            hero.style.display = 'none';
            list.style.display = 'none';
            restCard.hidden = false;
            finishBtn.hidden = !!session.completedAt;
            if (session.completedAt) {
                finishBtn.hidden = true;
            } else {
                finishBtn.hidden = true; // rest day: completion handled by skip-rest button
            }
            return;
        }

        hero.style.display = '';
        list.style.display = '';
        restCard.hidden = true;

        renderExerciseList(session);
        renderHeroProgress(session);

        finishBtn.hidden = false;
        const complete = isSessionComplete(session);
        finishBtn.textContent = complete ? 'WORKOUT COMPLETE ✓' : 'FINISH WORKOUT';
        finishBtn.classList.toggle('complete', complete);
        finishBtn.disabled = !complete && session.exercises.some((e) => !e.done);
        // Always allow click — clicking when not all done will mark all and finish
    }

    function renderHeroProgress(session) {
        const total = session.exercises.length;
        const done = session.exercises.filter((e) => e.done).length;
        const pct = total > 0 ? (done / total) * 100 : 0;

        $('#hero-progress-fill').style.width = pct + '%';
        $('#hero-completed-count').textContent = `${done} / ${total}`;

        const status = $('#hero-status');
        const hero = $('#workout-hero');
        if (done === 0) {
            status.textContent = "Let's go";
            hero.classList.remove('complete');
        } else if (done === total) {
            status.textContent = 'Complete!';
            hero.classList.add('complete');
        } else {
            status.textContent = `${total - done} to go`;
            hero.classList.remove('complete');
        }
    }

    function renderExerciseList(session) {
        const list = $('#exercise-list');
        list.innerHTML = '';

        session.exercises.forEach((ex, i) => {
            const card = document.createElement('div');
            card.className = 'exercise-card' + (ex.done ? ' done' : '');

            // Checkbox button
            const check = document.createElement('button');
            check.type = 'button';
            check.className = 'ex-check';
            check.setAttribute('aria-label', ex.done ? 'Mark incomplete' : 'Mark complete');
            check.innerHTML = '<svg viewBox="0 0 24 24"><path d="M5 12l4 4 10-10" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
            check.addEventListener('click', () => {
                ex.done = !ex.done;
                save();
                renderToday();
                renderStreak();
            });

            // Info
            const info = document.createElement('div');
            info.className = 'ex-info';
            const name = document.createElement('div');
            name.className = 'ex-name';
            const nameText = document.createElement('span');
            nameText.textContent = ex.name;
            const demoBtn = document.createElement('button');
            demoBtn.type = 'button';
            demoBtn.className = 'ex-demo-btn';
            demoBtn.title = `How to do ${ex.name}`;
            demoBtn.setAttribute('aria-label', `How to do ${ex.name}`);
            demoBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
            demoBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const q = encodeURIComponent(ex.name + ' proper form');
                window.open(`https://www.youtube.com/results?search_query=${q}`, '_blank', 'noopener');
            });
            name.appendChild(nameText);
            name.appendChild(demoBtn);
            const presc = document.createElement('div');
            presc.className = 'ex-prescribed';
            const badge = document.createElement('span');
            badge.className = 'badge';
            badge.textContent = ex.category;
            const prescText = document.createElement('span');
            prescText.textContent = `${ex.prescribedSets} × ${ex.prescribedReps}`;
            presc.appendChild(badge);
            presc.appendChild(prescText);
            info.appendChild(name);
            info.appendChild(presc);

            // Controls
            const controls = document.createElement('div');
            controls.className = 'ex-controls';
            if (!ex.noWeight) {
                const wInput = document.createElement('input');
                wInput.type = 'number';
                wInput.className = 'ex-weight-input';
                wInput.placeholder = '0';
                wInput.step = '0.5';
                wInput.min = '0';
                wInput.inputMode = 'decimal';
                wInput.value = ex.weight || '';
                wInput.title = 'Weight used';
                wInput.addEventListener('change', () => {
                    ex.weight = parseFloat(wInput.value) || 0;
                    save();
                });
                wInput.addEventListener('click', (e) => e.stopPropagation());
                const unit = document.createElement('span');
                unit.className = 'ex-unit';
                unit.textContent = state.settings.units;
                controls.appendChild(wInput);
                controls.appendChild(unit);
            }

            card.appendChild(check);
            card.appendChild(info);
            card.appendChild(controls);
            list.appendChild(card);
        });
    }

    function initFinishBtn() {
        $('#finish-btn').addEventListener('click', () => {
            const date = todayISO();
            const session = getOrCreateSession(date);
            if (!isSessionComplete(session)) {
                if (!confirm('Some exercises aren\'t checked off. Mark workout complete anyway?')) return;
                session.exercises.forEach((e) => { e.done = true; });
            }
            session.completedAt = new Date().toISOString();
            save();
            renderAll();
        });

        $('#skip-rest-btn').addEventListener('click', () => {
            // Acknowledge rest day OR replace today's session with the next non-rest day
            const date = todayISO();
            const session = getOrCreateSession(date);
            session.completedAt = new Date().toISOString();
            save();
            renderAll();
        });
    }

    // ============ WEIGH-IN ============
    function renderWeighIn() {
        const today = todayISO();
        const todayEntry = state.weights.find((w) => w.date === today);
        const status = $('#weigh-in-status');
        const input = $('#weight-value');

        $('#weigh-in-unit').textContent = state.settings.units;

        if (todayEntry) {
            status.textContent = `Logged: ${fmtWeight(todayEntry.value)} ${state.settings.units}`;
            status.classList.add('logged');
            input.value = todayEntry.value;
        } else {
            status.textContent = 'Not logged';
            status.classList.remove('logged');
        }
    }

    function initWeightForm() {
        $('#weight-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const date = todayISO();
            const value = parseFloat($('#weight-value').value);
            if (isNaN(value) || value <= 0) return;

            state.weights = state.weights.filter((w) => w.date !== date);
            state.weights.push({ id: uid(), date, value });
            save();
            renderAll();
        });
    }

    // ============ GOAL BANNER ============
    function renderGoalBanner() {
        const { settings } = state;
        const sorted = sortedWeights();
        const latest = sorted[sorted.length - 1];
        const current = latest ? latest.value : settings.startWeight;
        const target = settings.startWeight - settings.targetLoss;
        const toGo = Math.max(0, current - target);
        const daysLeft = settings.targetDate ? Math.max(0, daysBetween(todayISO(), settings.targetDate)) : 0;
        const lost = Math.max(0, settings.startWeight - current);
        const pct = settings.targetLoss > 0 ? Math.min(100, (lost / settings.targetLoss) * 100) : 0;

        // Ring math: r=34, circumference ≈ 213.6
        const circ = 2 * Math.PI * 34;
        const offset = circ * (1 - pct / 100);
        $('#goal-ring').setAttribute('stroke-dashoffset', offset);
        $('#goal-ring-pct').textContent = Math.round(pct) + '%';

        $('#goal-togo').textContent = settings.startWeight ? fmtWeight(toGo) : '—';
        $('#goal-togo-unit').textContent = settings.units;
        $('#goal-days').textContent = daysLeft;
        $('#goal-target-date').textContent = settings.targetDate ? fmtDate(settings.targetDate, { month: 'short', day: 'numeric' }) : '—';

        const pace = $('#goal-pace');
        pace.classList.remove('on-track', 'behind', 'far-behind');

        if (!settings.startWeight) {
            pace.textContent = 'Set your goal in Settings';
            return;
        }
        if (toGo <= 0) {
            pace.textContent = 'Goal reached!';
            pace.classList.add('on-track');
            return;
        }
        if (daysLeft <= 0) {
            pace.textContent = `${fmtWeight(toGo)} ${settings.units} short of goal`;
            pace.classList.add('behind');
            return;
        }
        const lbsPerWeek = (toGo / daysLeft) * 7;
        if (sorted.length >= 2) {
            const first = sorted[0];
            const elapsed = Math.max(1, daysBetween(first.date, latest.date));
            const actualPerWeek = ((first.value - latest.value) / elapsed) * 7;
            if (actualPerWeek >= lbsPerWeek * 0.9) {
                pace.textContent = `On pace · ${actualPerWeek.toFixed(2)} ${settings.units}/wk`;
                pace.classList.add('on-track');
            } else if (actualPerWeek > 0) {
                pace.textContent = `Behind · need ${lbsPerWeek.toFixed(2)} ${settings.units}/wk`;
                pace.classList.add('behind');
            } else {
                pace.textContent = `Off pace · need ${lbsPerWeek.toFixed(2)} ${settings.units}/wk`;
                pace.classList.add('far-behind');
            }
        } else {
            pace.textContent = `Need ${lbsPerWeek.toFixed(2)} ${settings.units}/wk`;
        }
    }

    // ============ STREAK ============
    function renderStreak() {
        const streak = getStreak();
        $('#streak-count').textContent = streak;
        $('#streak-badge').classList.toggle('active', streak > 0);
    }

    // ============ PROGRESS PANEL ============
    function renderProgressStats() {
        const { settings } = state;
        const sorted = sortedWeights();
        const latest = sorted[sorted.length - 1];
        const current = latest ? latest.value : settings.startWeight;
        const target = settings.startWeight - settings.targetLoss;
        const lost = Math.max(0, settings.startWeight - current);

        $('#stat-current').textContent = settings.startWeight ? fmtWeight(current) : '—';
        $('#stat-current-unit').textContent = settings.units;
        $('#stat-lost').textContent = settings.startWeight ? fmtWeight(lost) : '—';
        $('#stat-lost-unit').textContent = settings.units;
        $('#stat-target').textContent = settings.startWeight ? fmtWeight(target) : '—';
        $('#stat-target-unit').textContent = settings.units;

        // Workout stats
        const today = todayISO();
        const sevenAgo = new Date(); sevenAgo.setDate(sevenAgo.getDate() - 7);
        const thirtyAgo = new Date(); thirtyAgo.setDate(thirtyAgo.getDate() - 30);
        const isoSeven = sevenAgo.toISOString().slice(0, 10);
        const isoThirty = thirtyAgo.toISOString().slice(0, 10);

        let weekCount = 0, monthCount = 0, monthVolume = 0;
        state.sessions.forEach((s) => {
            if (!isSessionComplete(s) || s.isRest) return;
            if (s.date >= isoSeven && s.date <= today) weekCount++;
            if (s.date >= isoThirty && s.date <= today) {
                monthCount++;
                s.exercises.forEach((e) => {
                    if (!e.done) return;
                    const reps = (Number(e.actualReps) || 0) * (Number(e.prescribedSets) || 0);
                    const w = Number(e.weight) || 0;
                    monthVolume += w > 0 ? w * reps : reps;
                });
            }
        });

        $('#stat-week').textContent = weekCount;
        $('#stat-month').textContent = monthCount;
        $('#stat-volume').textContent = Math.round(monthVolume).toLocaleString();
        $('#stat-volume-unit').textContent = `${settings.units}·reps`;
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

        const xFor = (iso) => totalDays <= 0 ? padL + innerW / 2 : padL + (daysBetween(startDate, iso) / totalDays) * innerW;
        const yFor = (v) => padT + ((max - v) / range) * innerH;

        const ns = 'http://www.w3.org/2000/svg';

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
            label.setAttribute('fill', '#00d9a3');
            label.textContent = `target ${target.toFixed(1)}`;
            svg.appendChild(label);
        }

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

        sorted.forEach((w) => {
            const c = document.createElementNS(ns, 'circle');
            c.setAttribute('class', 'data-point');
            c.setAttribute('cx', xFor(w.date));
            c.setAttribute('cy', yFor(w.value));
            c.setAttribute('r', 4);
            const title = document.createElementNS(ns, 'title');
            title.textContent = `${fmtDate(w.date)}: ${fmtWeight(w.value)} ${state.settings.units}`;
            c.appendChild(title);
            svg.appendChild(c);
        });

        const lblStart = document.createElementNS(ns, 'text');
        lblStart.setAttribute('class', 'axis-label');
        lblStart.setAttribute('x', padL);
        lblStart.setAttribute('y', H - 8);
        lblStart.textContent = fmtDate(startDate, { month: 'short', day: 'numeric' });
        svg.appendChild(lblStart);

        if (startDate !== endDate) {
            const lblEnd = document.createElementNS(ns, 'text');
            lblEnd.setAttribute('class', 'axis-label');
            lblEnd.setAttribute('x', W - padR);
            lblEnd.setAttribute('y', H - 8);
            lblEnd.setAttribute('text-anchor', 'end');
            lblEnd.textContent = fmtDate(endDate, { month: 'short', day: 'numeric' });
            svg.appendChild(lblEnd);
        }
    }

    function renderHeatmap() {
        const wrap = $('#heatmap');
        wrap.innerHTML = '';
        const today = todayISO();
        const todayDate = new Date(today + 'T00:00:00');

        // Show last 12 weeks ending this Saturday
        const endDate = new Date(todayDate);
        endDate.setDate(endDate.getDate() + (6 - endDate.getDay())); // Saturday
        const weeks = 12;
        const startDate = new Date(endDate);
        startDate.setDate(startDate.getDate() - (weeks * 7 - 1));

        const sessionsByDate = {};
        state.sessions.forEach((s) => { sessionsByDate[s.date] = s; });

        for (let i = 0; i < weeks * 7; i++) {
            const d = new Date(startDate);
            d.setDate(d.getDate() + i);
            const iso = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

            const cell = document.createElement('div');
            cell.className = 'heat-cell';

            if (iso > today) {
                cell.classList.add('future');
                cell.title = fmtDate(iso);
            } else {
                const s = sessionsByDate[iso];
                const idx = getDayIndex(iso);
                const isRestDay = PROGRAM[idx].rest;
                if (s && isSessionComplete(s)) {
                    const ratio = s.exercises.length > 0
                        ? s.exercises.filter((e) => e.done).length / s.exercises.length
                        : 1;
                    if (ratio >= 1) cell.classList.add('l3');
                    else if (ratio >= 0.66) cell.classList.add('l2');
                    else if (ratio > 0) cell.classList.add('l1');
                    cell.title = `${fmtDate(iso)} — ${s.dayName}`;
                } else if (isRestDay) {
                    cell.classList.add('l1');
                    cell.title = `${fmtDate(iso)} — Rest`;
                } else {
                    cell.title = `${fmtDate(iso)} — missed`;
                }
            }
            if (iso === today) cell.classList.add('today');
            wrap.appendChild(cell);
        }
    }

    // ============ HISTORY ============
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

        const reversed = [...sorted].reverse();
        reversed.forEach((entry, i) => {
            const prev = reversed[i + 1];
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

    function renderSessionHistory() {
        const wrap = $('#session-history');
        const empty = $('#session-empty');
        wrap.innerHTML = '';

        const completed = state.sessions
            .filter((s) => isSessionComplete(s))
            .sort((a, b) => b.date.localeCompare(a.date));

        if (completed.length === 0) {
            empty.classList.remove('hidden');
            return;
        }
        empty.classList.add('hidden');

        completed.forEach((s) => {
            const card = document.createElement('div');
            card.className = 'session-card';

            const head = document.createElement('div');
            head.className = 'session-card-head';
            const date = document.createElement('span');
            date.className = 'session-date';
            date.textContent = fmtDate(s.date);
            const name = document.createElement('span');
            name.className = 'session-name';
            name.textContent = s.dayName;
            head.appendChild(date);
            head.appendChild(name);
            card.appendChild(head);

            if (s.isRest) {
                const note = document.createElement('div');
                note.style.color = 'var(--text-dim)';
                note.style.fontSize = '0.85rem';
                note.textContent = 'Rest day acknowledged';
                card.appendChild(note);
            } else {
                const ul = document.createElement('ul');
                ul.className = 'session-exercises';
                s.exercises.forEach((e) => {
                    const li = document.createElement('li');
                    if (!e.done) li.classList.add('skipped');
                    const lbl = document.createElement('span');
                    lbl.textContent = e.name;
                    const detail = document.createElement('span');
                    detail.className = 'ex-detail-text';
                    const wPart = e.weight > 0 ? ` @ ${fmtWeight(e.weight)} ${state.settings.units}` : '';
                    detail.textContent = `${e.prescribedSets} × ${e.prescribedReps}${wPart}`;
                    li.appendChild(lbl);
                    li.appendChild(detail);
                    ul.appendChild(li);
                });
                card.appendChild(ul);
            }

            wrap.appendChild(card);
        });
    }

    // ============ SETTINGS ============
    function loadSettingsForm() {
        $('#s-start').value = state.settings.startWeight || '';
        $('#s-loss').value = state.settings.targetLoss;
        $('#s-date').value = state.settings.targetDate;
        $('#s-units').value = state.settings.units;
        $('#s-program-start').value = state.settings.programStart || todayISO();
    }

    function renderProgramList() {
        const ol = $('#program-list');
        ol.innerHTML = '';
        PROGRAM.forEach((day, i) => {
            const li = document.createElement('li');
            li.className = 'program-day';

            const head = document.createElement('div');
            head.className = 'program-day-head';
            const num = document.createElement('span');
            num.className = 'program-day-num';
            num.textContent = `DAY ${i + 1}`;
            const name = document.createElement('span');
            name.className = 'program-day-name';
            name.textContent = day.name;
            head.appendChild(num);
            head.appendChild(name);
            li.appendChild(head);

            if (day.rest) {
                const p = document.createElement('p');
                p.style.margin = '0';
                p.style.color = 'var(--text-dim)';
                p.style.fontSize = '0.85rem';
                p.textContent = 'Recovery day — no prescribed exercises.';
                li.appendChild(p);
            } else {
                const ul = document.createElement('ul');
                ul.className = 'program-day-list';
                day.exercises.forEach((e) => {
                    const item = document.createElement('li');
                    const txt = document.createElement('span');
                    txt.textContent = `${e.name} — ${e.sets} × ${e.reps}`;
                    const demoBtn = document.createElement('button');
                    demoBtn.type = 'button';
                    demoBtn.className = 'ex-demo-btn small';
                    demoBtn.title = `How to do ${e.name}`;
                    demoBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
                    demoBtn.addEventListener('click', () => {
                        const q = encodeURIComponent(e.name + ' proper form');
                        window.open(`https://www.youtube.com/results?search_query=${q}`, '_blank', 'noopener');
                    });
                    item.appendChild(txt);
                    item.appendChild(demoBtn);
                    ul.appendChild(item);
                });
                li.appendChild(ul);
            }
            ol.appendChild(li);
        });
    }

    function initSettings() {
        if (!state.settings.programStart) {
            state.settings.programStart = todayISO();
            save();
        }
        loadSettingsForm();

        $('#settings-form').addEventListener('submit', (e) => {
            e.preventDefault();
            state.settings.startWeight = parseFloat($('#s-start').value) || 0;
            state.settings.targetLoss = parseFloat($('#s-loss').value) || 0;
            state.settings.targetDate = $('#s-date').value;
            state.settings.units = $('#s-units').value;
            state.settings.programStart = $('#s-program-start').value || todayISO();
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
            a.download = `forge-${todayISO()}.json`;
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
                    state = {
                        settings: { ...defaultState.settings, ...(imported.settings || {}) },
                        weights: Array.isArray(imported.weights) ? imported.weights : [],
                        sessions: Array.isArray(imported.sessions) ? imported.sessions : [],
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
            if (!confirm('Delete ALL data — weight log, workouts, settings? This cannot be undone.')) return;
            localStorage.removeItem(STORAGE_KEY);
            state = load();
            state.settings.programStart = todayISO();
            save();
            loadSettingsForm();
            renderAll();
        });
    }

    // ============ RENDER ALL ============
    function renderAll() {
        renderToday();
        renderWeighIn();
        renderGoalBanner();
        renderStreak();
        renderProgressStats();
        renderChart();
        renderHeatmap();
        renderWeightTable();
        renderSessionHistory();
    }

    // ============ INIT ============
    initTabs();
    initFinishBtn();
    initWeightForm();
    initSettings();
    renderProgramList();
    renderAll();
})();
