/**
 * PeakPulse — Study Timer
 * Countdown timer with presets, start/pause/reset, and session saving
 */

document.addEventListener('DOMContentLoaded', () => {
  // ─── Elements ──────────────────────────────────────────────────
  const timeDisplay = document.getElementById('timer-time');
  const timerDisplayContainer = document.getElementById('timer-display');
  const startBtn = document.getElementById('timer-start');
  const pauseBtn = document.getElementById('timer-pause');
  const resetBtn = document.getElementById('timer-reset');
  const presetBtns = document.querySelectorAll('.preset-btn');
  const taskSelect = document.getElementById('timer-task');
  const ringProgress = document.getElementById('timer-ring-progress');
  const todayTotal = document.getElementById('today-total');

  // ─── State ─────────────────────────────────────────────────────
  let totalSeconds = 25 * 60; // Default 25 min
  let remainingSeconds = totalSeconds;
  let interval = null;
  let isRunning = false;
  let elapsedWhenStopped = 0;

  // ─── Display ───────────────────────────────────────────────────
  function updateDisplay() {
    const mins = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    timeDisplay.textContent =
      String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');

    // Update ring rotation based on progress
    const progress = 1 - remainingSeconds / totalSeconds;
    const degrees = progress * 360;
    ringProgress.style.transform = `rotate(${degrees}deg)`;
  }

  function setPreset(minutes) {
    totalSeconds = minutes * 60;
    remainingSeconds = totalSeconds;
    elapsedWhenStopped = 0;
    updateDisplay();
  }

  // ─── Timer Controls ────────────────────────────────────────────
  function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timerDisplayContainer.classList.add('running');
    startBtn.style.display = 'none';
    pauseBtn.style.display = '';

    interval = setInterval(() => {
      if (remainingSeconds <= 0) {
        stopTimer();
        handleTimerEnd();
        return;
      }
      remainingSeconds--;
      elapsedWhenStopped++;
      updateDisplay();
    }, 1000);
  }

  function pauseTimer() {
    if (!isRunning) return;
    isRunning = false;
    timerDisplayContainer.classList.remove('running');
    clearInterval(interval);
    interval = null;
    startBtn.style.display = '';
    pauseBtn.style.display = 'none';
    startBtn.innerHTML = '▶️ Resume';
  }

  function stopTimer() {
    isRunning = false;
    timerDisplayContainer.classList.remove('running');
    clearInterval(interval);
    interval = null;
    startBtn.style.display = '';
    pauseBtn.style.display = 'none';
    startBtn.innerHTML = '▶️ Start';
  }

  function resetTimer() {
    // Save session if any time was recorded
    if (elapsedWhenStopped >= 5) {
      saveSession(elapsedWhenStopped);
    }
    stopTimer();
    remainingSeconds = totalSeconds;
    elapsedWhenStopped = 0;
    updateDisplay();
  }

  function handleTimerEnd() {
    // Save the full session
    saveSession(totalSeconds);
    elapsedWhenStopped = 0;

    // Alert user
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('⏱️ PeakPulse Timer', {
        body: 'Time is up! Great work! 🎉',
      });
    }
    alert('⏰ Time is up! Great work! 🎉');

    // Reset display
    remainingSeconds = totalSeconds;
    updateDisplay();
  }

  // ─── Save Session ──────────────────────────────────────────────
  async function saveSession(duration) {
    try {
      const taskId = taskSelect.value || null;
      const res = await fetch('/api/timer/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration, task_id: taskId }),
      });
      const data = await res.json();
      if (data.success) {
        // Update today's total display
        updateTodayTotal(duration);
      }
    } catch (err) {
      console.error('Failed to save session:', err);
    }
  }

  function updateTodayTotal(additionalSeconds) {
    // Parse current display and add
    const current = todayTotal.textContent.trim();
    let totalMins = 0;

    const hMatch = current.match(/(\d+)h/);
    const mMatch = current.match(/(\d+)m/);
    if (hMatch) totalMins += parseInt(hMatch[1]) * 60;
    if (mMatch) totalMins += parseInt(mMatch[1]);

    totalMins += Math.floor(additionalSeconds / 60);

    const h = Math.floor(totalMins / 60);
    const m = totalMins % 60;
    todayTotal.textContent = (h > 0 ? h + 'h ' : '') + m + 'm';
  }

  // ─── Event Listeners ──────────────────────────────────────────
  startBtn.addEventListener('click', startTimer);
  pauseBtn.addEventListener('click', pauseTimer);
  resetBtn.addEventListener('click', resetTimer);

  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (isRunning) return; // Don't change preset while running

      presetBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      setPreset(parseInt(btn.dataset.minutes));
    });
  });

  // Request notification permission
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }

  // Prevent accidental page close during timer
  window.addEventListener('beforeunload', (e) => {
    if (isRunning) {
      e.preventDefault();
      e.returnValue = 'Timer is running! Are you sure you want to leave?';
    }
  });

  // ─── Initialize ────────────────────────────────────────────────
  updateDisplay();
});
