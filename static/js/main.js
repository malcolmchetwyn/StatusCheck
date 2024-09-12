/*
 Author: Malcolm
*/

// Define the fields for each section
const sectionFields = {
   wakeUp: ['wake_up_mental', 'wake_up_emotional', 'wake_up_physical'],
   postBreakfast: ['post_breakfast_mental', 'post_breakfast_emotional', 'post_breakfast_physical', 'post_breakfast_extra'],
   postLunch: ['post_lunch_mental', 'post_lunch_emotional', 'post_lunch_physical', 'post_lunch_extra'],
   postDinner: ['post_dinner_mental', 'post_dinner_emotional', 'post_dinner_physical', 'post_dinner_extra'],
   bedtime: ['bedtime_mental', 'bedtime_emotional', 'bedtime_physical'],
   notes: ['notes_observations'],
   exercise: ['exercise_details']
};

const sectionIds = Object.keys(sectionFields);

function startDictation(inputId) {
   if ('webkitSpeechRecognition' in window) {
      const recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.lang = 'en-US';
      recognition.start();

      recognition.onresult = function (event) {
         document.getElementById(inputId).value = event.results[0][0].transcript;
         recognition.stop();
      };

      recognition.onerror = function () {
         recognition.stop();
      };
   } else {
      alert("Speech recognition is not supported in this browser. Please try using Chrome or another supported browser.");
   }
}

document.addEventListener('DOMContentLoaded', function () {
   const today = new Date().toISOString().split('T')[0];
   document.getElementById('date-picker').value = today; // Set the date picker to today's date
   document.getElementById('selected-date').innerText = "Today";
   loadData(today); // Load data for today initially
});

function loadDataForDate() {
   const selectedDate = document.getElementById('date-picker').value;
   if (!selectedDate) {
      alert("Please select a date.");
      return;
   }
   document.getElementById('selected-date').innerText = (selectedDate === new Date().toISOString().split('T')[0]) ? "Today" : selectedDate;
   loadData(selectedDate); // Now using the selected date for loading data
}

function loadData(date) {
   if (!date) {
      console.error("No date provided for fetching data.");
      alert("Please select a valid date.");
      return;
   }

   fetch(`/status/${date}`)
      .then(response => {
         if (!response.ok) {
            throw new Error("Failed to fetch data for the selected date.");
         }
         return response.json();
      })
      .then(data => {
         console.log("Fetched data for date:", data); // Debugging line

         // Reset all headers first
         resetAllHeaders();

         if (Object.keys(data).length > 0) {
            // Populate fields with the retrieved data
            for (const sectionId in sectionFields) {
               sectionFields[sectionId].forEach(fieldId => {
                  document.getElementById(fieldId).value = data[fieldId] || '';
               });
               // Check if section is completed after populating
               checkIfSectionCompleted(sectionId);
            }

            // Update the progress bar
            updateProgressBarFromData();
         } else {
            alert("No data found for the selected date.");
            clearFields();
            resetProgressBar();
         }
      })
      .catch(error => {
         console.error('Error fetching data for selected date:', error);
         alert('Error fetching data for selected date.');
      });
}

function resetAllHeaders() {
   sectionIds.forEach(sectionId => {
      const cardHeader = document.querySelector(`#heading${sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}`);

      // Reset the header background and text color to default
      cardHeader.style.backgroundColor = '';
      cardHeader.style.color = ''; // Reset text color
   });
}

function clearFields() {
   for (const sectionId in sectionFields) {
      sectionFields[sectionId].forEach(fieldId => {
         document.getElementById(fieldId).value = '';
      });
   }
}

// Function to update the progress bar based on completed sections
function updateProgressBarFromData() {
   let completedSections = 0;

   sectionIds.forEach(sectionId => {
      const isCompleted = checkIfSectionCompleted(sectionId, false); // Do not collapse on check
      if (isCompleted) {
         completedSections++;
      }
   });

   const progressBar = document.getElementById('progress-bar');
   const progressPercentage = (completedSections / sectionIds.length) * 100;
   progressBar.style.width = `${progressPercentage}%`;

   // If 100% progress, change the color to green
   if (progressPercentage === 100) {
      progressBar.style.backgroundColor = '#41b658';
   } else {
      // Reset to the default color (bootstrap blue)
      progressBar.style.backgroundColor = '';
   }
}

// Function to reset the progress bar to 0% without animation
function resetProgressBar() {
   const progressBar = document.getElementById('progress-bar');

   // Temporarily disable transition to remove animation
   progressBar.style.transition = 'none';

   // Set progress bar width to 0%
   progressBar.style.width = '0%';

   // Allow the browser to render the change
   setTimeout(() => {
      // Re-enable transition for future progress bar updates
      progressBar.style.transition = '';
   }, 10); // Small delay to ensure rendering happens before transition is re-enabled
}

function gatherSectionData(sectionId) {
   const selectedDate = document.getElementById('date-picker').value || new Date().toISOString().split('T')[0];
   const data = {
      date: selectedDate
   };

   if (!sectionFields[sectionId]) {
      return null;
   }

   sectionFields[sectionId].forEach(fieldId => {
      data[fieldId] = document.getElementById(fieldId).value || null;
   });

   return data;
}

function submitSection(sectionId) {
   const sectionData = gatherSectionData(sectionId);
   console.log("Section Data being submitted:", sectionData);

   if (!sectionData) {
      alert("Please fill in all required fields.");
      return;
   }

   fetch('/status', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify(sectionData),
      })
      .then(response => {
         if (!response.ok) {
            throw new Error("Network response was not ok");
         }
         return response.json();
      })
      .then(data => {
         console.log("Response from server:", data);
         if (data.message) {
            alert(`${sectionId} data saved successfully.`);
            checkIfSectionCompleted(sectionId);

            // Re-fetch data for the selected date
            const selectedDate = document.getElementById('date-picker').value;
            loadData(selectedDate);
         } else {
            alert('Failed to save the data.');
         }
      })
      .catch((error) => {
         console.error('Error:', error);
         alert('An error occurred. Please try again.');
      });
}

// Function to check if all fields in a section are completed
function checkIfSectionCompleted(sectionId, shouldCollapse = true) {
   let isCompleted = true;

   if (!sectionFields[sectionId]) {
      return false;
   }

   sectionFields[sectionId].forEach(fieldId => {
      const input = document.getElementById(fieldId);
      if (!input.value || input.value.trim() === '') {
         isCompleted = false;
      }
   });

   const cardHeader = document.querySelector(`#heading${sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}`);

   if (isCompleted) {
      // Set the header background to green and text color to white
      cardHeader.style.backgroundColor = '#41b658d4';
      cardHeader.style.color = 'white'; // Set text color to white

      // Optionally collapse the section if completed
      if (shouldCollapse) {
         $(`#${sectionId}`).collapse('hide');
      }
   } else {
      // Reset header to default color if not completed
      cardHeader.style.backgroundColor = '';
      cardHeader.style.color = '';
   }

   return isCompleted; // Return the completion status of the section
}
