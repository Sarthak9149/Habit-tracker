const calendarIcon = document.getElementById('calendar-icon');
        const calendarModal = document.getElementById('calendar-modal');
        const calendarOverlay = document.getElementById('calendar-overlay');
        const dateCells = document.querySelectorAll('.date-cell');

        // Function to toggle calendar visibility
        function toggleCalendar() {
            const isVisible = calendarModal.style.display === 'block';
            calendarModal.style.display = isVisible ? 'none' : 'block';
            calendarOverlay.style.display = isVisible ? 'none' : 'block';
        }

        // Add event listeners
        calendarIcon.addEventListener('click', toggleCalendar);
        calendarOverlay.addEventListener('click', toggleCalendar);

        dateCells.forEach(cell => {
            cell.addEventListener('click', () => {
                // Check if the date is already tracked
                if (cell.classList.contains('bg-green-500')) {
                    // Untrack the habit: change to gray background and black text
                    cell.classList.remove('bg-green-500', 'text-white');
                    cell.classList.add('bg-gray-100', 'text-gray-700');
                } else {
                    // Track the habit: change to green background and white text
                    cell.classList.remove('bg-gray-100', 'text-gray-700');
                    cell.classList.add('bg-green-500', 'text-white');
                }
            });
        });