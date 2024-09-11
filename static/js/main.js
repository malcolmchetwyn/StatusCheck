/*
 Author: Malcolm
*/

function startDictation(inputId) {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
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
 
    fetch(`/status/${date}`) // Ensuring we make the request with a valid date
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
             document.getElementById('wake_up_mental').value = data.wake_up_mental || '';
             document.getElementById('wake_up_emotional').value = data.wake_up_emotional || '';
             document.getElementById('wake_up_physical').value = data.wake_up_physical || '';
 
             // Post Breakfast Fields
             document.getElementById('post_breakfast_mental').value = data.post_breakfast_mental || '';
             document.getElementById('post_breakfast_emotional').value = data.post_breakfast_emotional || '';
             document.getElementById('post_breakfast_physical').value = data.post_breakfast_physical || '';
             document.getElementById('post_breakfast_extra').value = data.post_breakfast_extra || ''; 
 
             // Post Lunch Fields
             document.getElementById('post_lunch_mental').value = data.post_lunch_mental || '';
             document.getElementById('post_lunch_emotional').value = data.post_lunch_emotional || '';
             document.getElementById('post_lunch_physical').value = data.post_lunch_physical || '';
             document.getElementById('post_lunch_extra').value = data.post_lunch_extra || ''; 
 
             // Post Dinner Fields
             document.getElementById('post_dinner_mental').value = data.post_dinner_mental || '';
             document.getElementById('post_dinner_emotional').value = data.post_dinner_emotional || '';
             document.getElementById('post_dinner_physical').value = data.post_dinner_physical || '';
             document.getElementById('post_dinner_extra').value = data.post_dinner_extra || ''; 
 
             // Bedtime Fields
             document.getElementById('bedtime_mental').value = data.bedtime_mental || '';
             document.getElementById('bedtime_emotional').value = data.bedtime_emotional || '';
             document.getElementById('bedtime_physical').value = data.bedtime_physical || '';
 
             // Notes and Exercise
             document.getElementById('notes_observations').value = data.notes_observations || '';
             document.getElementById('exercise_details').value = data.exercise_details || '';
 
 
             // Call checkIfSectionCompleted for each section after populating
             checkIfSectionCompleted('wakeUp');
             checkIfSectionCompleted('postBreakfast');
             checkIfSectionCompleted('postLunch');
             checkIfSectionCompleted('postDinner');
             checkIfSectionCompleted('bedtime');
             checkIfSectionCompleted('notes');
             checkIfSectionCompleted('exercise');
 
             // Update the progress bar
             updateProgressBarFromData(data);
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
    const sectionIds = ['wakeUp', 'postBreakfast', 'postLunch', 'postDinner', 'bedtime', 'notes', 'exercise'];
    sectionIds.forEach(sectionId => {
       const cardHeader = document.querySelector(`#heading${sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}`);
       const button = cardHeader.querySelector('button');
 
       // Reset the header background and button text to default
       cardHeader.style.backgroundColor = '';
       button.style.color = ''; // Reset button text color
    });
 }
 
 
 function clearFields() {
    document.getElementById('wake_up_mental').value = '';
    document.getElementById('wake_up_emotional').value = '';
    document.getElementById('wake_up_physical').value = '';
    document.getElementById('post_breakfast_mental').value = '';
    document.getElementById('post_breakfast_emotional').value = '';
    document.getElementById('post_breakfast_physical').value = '';
    document.getElementById('post_lunch_mental').value = '';
    document.getElementById('post_lunch_emotional').value = '';
    document.getElementById('post_lunch_physical').value = '';
    document.getElementById('post_dinner_mental').value = '';
    document.getElementById('post_dinner_emotional').value = '';
    document.getElementById('post_dinner_physical').value = '';
    document.getElementById('bedtime_mental').value = '';
    document.getElementById('bedtime_emotional').value = '';
    document.getElementById('bedtime_physical').value = '';
    document.getElementById('notes_observations').value = '';
    document.getElementById('exercise_details').value = '';
 }
 
 
 // Function to update the progress bar only when all fields in a card are completed
 function updateProgressBarFromData(data) {
    const sectionIds = ['wakeUp', 'postBreakfast', 'postLunch', 'postDinner', 'bedtime', 'notes', 'exercise'];
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
    const selectedDate = document.getElementById('date-picker').value;
    const data = {
       date: selectedDate || new Date().toISOString().split('T')[0]
    };
 
    switch (sectionId) {
       case 'wakeUp':
          data.wake_up_mental = document.getElementById('wake_up_mental').value || null;
          data.wake_up_emotional = document.getElementById('wake_up_emotional').value || null;
          data.wake_up_physical = document.getElementById('wake_up_physical').value || null;
          break;
       case 'postBreakfast':
          data.post_breakfast_mental = document.getElementById('post_breakfast_mental').value || null;
          data.post_breakfast_emotional = document.getElementById('post_breakfast_emotional').value || null;
          data.post_breakfast_physical = document.getElementById('post_breakfast_physical').value || null;
          data.post_breakfast_extra = document.getElementById('post_breakfast_extra').value || null;
          break;
       case 'postLunch':
          data.post_lunch_mental = document.getElementById('post_lunch_mental').value || null;
          data.post_lunch_emotional = document.getElementById('post_lunch_emotional').value || null;
          data.post_lunch_physical = document.getElementById('post_lunch_physical').value || null;
          data.post_lunch_extra = document.getElementById('post_lunch_extra').value || null;
          break;
       case 'postDinner':
          data.post_dinner_mental = document.getElementById('post_dinner_mental').value || null;
          data.post_dinner_emotional = document.getElementById('post_dinner_emotional').value || null;
          data.post_dinner_physical = document.getElementById('post_dinner_physical').value || null;
          data.post_dinner_extra = document.getElementById('post_dinner_extra').value || null;
          break;
       case 'bedtime':
          data.bedtime_mental = document.getElementById('bedtime_mental').value || null;
          data.bedtime_emotional = document.getElementById('bedtime_emotional').value || null;
          data.bedtime_physical = document.getElementById('bedtime_physical').value || null;
          break;
       case 'notes':
          data.notes_observations = document.getElementById('notes_observations').value || null;
          break;
       case 'exercise':
          data.exercise_details = document.getElementById('exercise_details').value || null;
          break;
       default:
          return null;
    }
 
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
             checkIfSectionCompleted(sectionId); // New function to check if section is completed
 
             // Re-fetch data for the selected date
             const selectedDate = document.getElementById('date-picker').value;
             loadData(selectedDate); // <--- This is the critical part. Ensure this fetch is correct.
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
    const inputs = document.querySelectorAll(`#${sectionId} input, #${sectionId} textarea`);
 
    // Check if all inputs have values
    inputs.forEach(input => {
       if (!input.value || input.value.trim() === '') {
          isCompleted = false;
       }
    });
 
    const cardHeader = document.querySelector(`#heading${sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}`);
    const button = cardHeader.querySelector('button');
 
    if (isCompleted) {
       // Set the header background to green and text color to white
       cardHeader.style.backgroundColor = '#41b658d4';
       button.style.color = 'white'; // Set button text color to white
 
       // Optionally collapse the section if completed
       if (shouldCollapse) {
          $(`#${sectionId}`).collapse('hide');
       }
    } else {
       // Reset header to default color if not completed
       cardHeader.style.backgroundColor = '';
       button.style.color = '';
    }
 
    return isCompleted; // Return the completion status of the section
 }