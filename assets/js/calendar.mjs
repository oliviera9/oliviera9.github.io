// ISO date-only keys avoid browser-timezone shifts for all-day walking activities.
export function localDateKey(now = new Date(), timeZone = 'Europe/Rome') {
  const parts = new Intl.DateTimeFormat('en', {
    timeZone, year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(now);
  const part = type => parts.find(value => value.type === type).value;
  return `${part('year')}-${part('month')}-${part('day')}`;
}
export function isUpcoming(endDate, today) {
  return endDate >= today;
}
export function enquirySelection(title, dates) {
  return `${title} · ${dates}`;
}

if (typeof document !== 'undefined') {
  const calendar = document.querySelector('[data-activity-calendar]');
  if (calendar) {
    function refreshDates() {
      const today = localDateKey(new Date(), calendar.dataset.timezone);
      calendar.querySelectorAll('[data-calendar-event]').forEach(event => {
        event.hidden = !isUpcoming(event.dataset.endDate, today);
      });
      calendar.querySelectorAll('[data-calendar-month]').forEach(month => {
        month.hidden = ![...month.querySelectorAll('[data-calendar-event]')].some(event => !event.hidden);
      });
      const hasEvents = [...calendar.querySelectorAll('[data-calendar-event]')].some(event => !event.hidden);
      calendar.querySelector('[data-calendar-empty]').hidden = hasEvents;
      calendar.querySelector('[data-calendar-note]').hidden = !hasEvents;
    }
    refreshDates();
    window.addEventListener('focus', refreshDates);
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) refreshDates();
    });
    window.setInterval(refreshDates, 60000);

    const form = document.querySelector('[data-enquiry-form]');
    if (form) {
      const selected = form.querySelector('[data-calendar-selection]');
      const summary = form.querySelector('[data-selected-activity]');
      const field = form.querySelector('[data-planned-activity]');
      const dates = form.querySelector('[name="dates"]');
      const kind = form.querySelector('[name="activity"]');
      let previousDates = '';
      let previousKind = '';
      let selectedDates = '';
      let selectedKind = '';
      function clearSelection() {
        if (!selected.hidden) {
          if (dates.value === selectedDates) dates.value = previousDates;
          if (kind.value === selectedKind) kind.value = previousKind;
        }
        selected.hidden = true;
        summary.textContent = '';
        field.value = '';
      }
      calendar.querySelectorAll('[data-planned-enquiry]').forEach(link => {
        link.addEventListener('click', () => {
          if (selected.hidden) {
            previousDates = dates.value;
            previousKind = kind.value;
          }
          selectedDates = link.dataset.eventDate;
          selectedKind = link.dataset.eventKind;
          const label = enquirySelection(link.dataset.eventTitle, selectedDates);
          summary.textContent = label;
          field.value = `${link.dataset.eventId}: ${label}`;
          selected.hidden = false;
          dates.value = selectedDates;
          kind.value = selectedKind;
        });
      });
      form.querySelector('[data-clear-activity]').addEventListener('click', () => {
        clearSelection();
        kind.focus();
      });
      document.querySelectorAll('[data-experience]').forEach(link => {
        link.addEventListener('click', () => {
          clearSelection();
          kind.value = link.dataset.experience;
        });
      });
    }
  }
}
