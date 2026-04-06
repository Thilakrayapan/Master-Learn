/**
 * PeakPulse — Task List Interactions
 * Client-side filtering and deadline set helper
 */

document.addEventListener('DOMContentLoaded', () => {
  // ─── Filter Tabs ──────────────────────────────────────────────
  const filterTabs = document.querySelectorAll('.filter-tab');
  const taskCards = document.querySelectorAll('.task-card');
  const emptyState = document.getElementById('empty-state');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Update active tab
      filterTabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      const filter = tab.dataset.filter;
      let visibleCount = 0;

      taskCards.forEach(card => {
        if (filter === 'all' || card.dataset.status === filter) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      // Show/hide empty state
      if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? '' : 'none';
      }
    });
  });

  // ─── Default Deadline ─────────────────────────────────────────
  const deadlineInput = document.getElementById('task-deadline');
  if (deadlineInput && !deadlineInput.value) {
    // Default: tomorrow at 11:59 PM
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(23, 59, 0, 0);
    const formatted = tomorrow.toISOString().slice(0, 16);
    deadlineInput.value = formatted;
    deadlineInput.min = new Date().toISOString().slice(0, 16);
  }

  // ─── Form Validation Feedback ─────────────────────────────────
  const taskForm = document.getElementById('task-form');
  if (taskForm) {
    taskForm.addEventListener('submit', (e) => {
      const title = document.getElementById('task-title').value.trim();
      const deadline = document.getElementById('task-deadline').value;

      if (!title || !deadline) {
        e.preventDefault();
        alert('Please fill in both the task title and deadline.');
      }
    });
  }

  // ─── Swipe-aware task cards (mobile enhancement) ──────────────
  // Re-trigger card entry animations on filter
  function reAnimateCards() {
    const visible = document.querySelectorAll('.task-card:not([style*="display: none"])');
    visible.forEach((card, i) => {
      card.style.animation = 'none';
      card.offsetHeight; // Trigger reflow
      card.style.animation = `fadeInUp 0.4s ease-out ${i * 0.05}s both`;
    });
  }

  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      setTimeout(reAnimateCards, 10);
    });
  });

  // ─── Format Local Times ───────────────────────────────────────
  const localTimeElements = document.querySelectorAll('.local-time');
  localTimeElements.forEach(el => {
    const isoString = el.getAttribute('datetime');
    if (isoString) {
      const date = new Date(isoString);
      if (!isNaN(date)) {
        const dateStr = date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
        const timeStr = date.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
        el.textContent = `${dateStr} at ${timeStr}`;
        // Set the tooltip to show exact timezone
        el.title = date.toLocaleString();
      }
    }
  });
});
