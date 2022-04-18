
// Display alert message on back/refresh.
// https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onbeforeunload
function verify_unload(e){
e.preventDefault();
(e || window.event).returnValue = null;
return null;
};
window.addEventListener("beforeunload", verify_unload);

// Define example survey.
var likert_page = {
type: 'survey-likert',
questions: [{prompt: "Are you seeing something right now?", labels: ["Yes", "No"]}],
on_start: function(data) {
    pass_message('message to pass to nivturk');
}
};

// Define global variables.
var low_quality = false;

// Initialize timeline.
var timeline = [likert_page];

jsPsych.init({
timeline: timeline,
on_finish: function() {

    // Remove requirement to verify redirect
    window.removeEventListener("beforeunload", verify_unload);

    // Add interactions to the data variable
    var interaction_data = jsPsych.data.getInteractionData();
    jsPsych.data.get().addToLast({interactions: interaction_data.json()});

    // Display jsPsych data in viewport.
    // jsPsych.data.displayData();

    if (low_quality) {

    // Save rejected dataset to disk.
    redirect_reject("{{workerId}}", "{{assignmentId}}", "{{hitId}}", "{{code_reject}}");

    } else {

    // Save complete dataset to disk.
    redirect_success("{{workerId}}", "{{assignmentId}}", "{{hitId}}", "{{code_success}}");

    }

}
})
