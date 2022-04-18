

// Display alert message on back/refresh.
// https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onbeforeunload

// // Define example survey.
// var likert_page = {
// type: 'survey-likert',
// questions: [{prompt: "Are you seeing something right now?", labels: ["Yes", "No"]}],
// on_start: function(data) {
//     pass_message('message to pass to nivturk');
// }
// };

// Define global variables.
var low_quality = false;

// // Initialize timeline.
// var timeline = [likert_page];



function verify_unload(e){
    e.preventDefault();
    (e || window.event).returnValue = null;
    return null;
};
window.addEventListener("beforeunload", verify_unload);


/* initialize jsPsych */
var jsPsych = initJsPsych({
on_finish: function() {
    jsPsych.data.displayData();

    // Remove requirement to verify redirect
    window.removeEventListener("beforeunload", verify_unload);

    // Add interactions to the data variable
    var interaction_data = jsPsych.data.getInteractionData();
    jsPsych.data.get().addToLast({interactions: interaction_data.json()});

    // Display jsPsych data in viewport.
    // jsPsych.data.displayData();
    var low_quality = false;

    if (low_quality) {

    // Save rejected dataset to disk.
    redirect_reject("{{workerId}}", "{{assignmentId}}", "{{hitId}}", "{{code_reject}}");

    } else {

    // Save complete dataset to disk.
    redirect_success("{{workerId}}", "{{assignmentId}}", "{{hitId}}", "{{code_success}}");

    }
},
extensions: [
    {type: jsPsychExtensionMouseTracking, params: {minimum_sample_time: 0}}
  ]
});

/* create timeline */
var timeline = [
    // 1- weclome page + instructions
    // 2- block 1 A
    // 3- block 2 B
    // 4- block 3 A-B
    // 5- block 4 C-D
    // (optional) - block 3 A-C, B-C, A-D, B-D
    // 6- survey (questions)

    // exp block:
        // 1- new task
        // 2- N trials (20)
        // 3- task description, how hard was it (subjective judgment) ?
        
        // trial
            // 1- fixation (1 second, not sure)
            // 2- stimuli presentation
            // 3- mouse tracking, eyegazer, expand on hover, choice selection
            // 4- uncertainty slider + submit
            // 5- feedback (button for next)

    // record browser interactions (when the participant isn't focusing)
];


// // the mouse tracking extension
// var trial = {
//     type: jsPsychHtmlButtonResponse,
//     // stimulus: '<div id="target" style="width:250px; height: 250px; background-color: #333; margin: auto;"></div>',
//     stimulus: '',
    
//     choices: ['1', '2', '3', '4'],
//     prompt: "<p>Where is the odd one out</p>",
//     extensions: [
//       {type: jsPsychExtensionMouseTracking, params: {targets: ['#target']}}
//     ],
//     data: {
//       task: 'draw'
//     }
//   };

/* preload images */


// var baseFolder = '../static/human_exp_images/'
// var tasks = "{{ tasks_names|tojson }}";
// var n_tasks = tasks.length;
// var n_trials = "{{ n_trials }}";


// var baseFolder = '/home/aimen/projects/cvrt_git/human_exp_images/'
// var baseFolder = '../../../cvrt_git/human_exp_images/'

// var tasks = ['task_count', 'task_inside', 'task_count_inside_1'];

// var n_tasks = 4;

// var n_trials = 3;

// var all_tasks = [{task_idx: 0}, {task_idx: 1}, {task_idx: 2}] 
// var tasks = {{ geocode|tojson }};

function load_task(baseFolder, task){
    var all_images = [];
    var preload_images = [];
    for (let i = 0; i < n_trials; i++) {
        var taskFolder = baseFolder + task + '/'
        
        all_images.push([
            taskFolder + pad(i, 2) + '_' + 0 + '.png', 
            taskFolder + pad(i, 2) + '_' + 1 + '.png', 
            taskFolder + pad(i, 2) + '_' + 2 + '.png', 
            taskFolder + pad(i, 2) + '_' + 3 + '.png'
        ]);

        // preload_images.push(taskFolder + pad(i, 2) + '_' + 0 + '.png');
        // preload_images.push(taskFolder + pad(i, 2) + '_' + 1 + '.png');
        // preload_images.push(taskFolder + pad(i, 2) + '_' + 2 + '.png');
        // preload_images.push(taskFolder + pad(i, 2) + '_' + 3 + '.png');
    }
    return all_images
}

var all_preload_images = []
var all_tasks_images = []
for (let i = 0; i < n_trials; i++) {
    var images = load_task(baseFolder, tasks[i])
    var preload_images = [].concat.apply([], images)
    all_tasks_images.push(images)
    all_preload_images.push(preload_images)
}

var preload_images = [].concat.apply([], all_preload_images)

/* define trial stimuli array for timeline variables */

var labelArray = [0,1,2,3];
var responses = ['h', 'j', 'b', 'n']

var all_test_stimuli = []

for (let k = 0; k < n_tasks; k++) {

    var test_stimuli = [];
    for (let i = 0; i < n_trials; i++) {

        var shuffledArray = jsPsych.randomization.shuffleNoRepeats(labelArray);
        var images = []
        for (let j = 0; j < 4; j++){
            if(shuffledArray[j] == 3){var indexCorrect=j;}
            images.push(all_tasks_images[k][i][shuffledArray[j]])
        }
        test_stimuli.push({
            // stimulus: all_images[i],
            stimulus: images,
            correct_response: indexCorrect,
            shuffled_array: shuffledArray,
        })
    }
    all_test_stimuli.push(test_stimuli)
}



var preload = {
type: jsPsychPreload,
images: preload_images
// ask server about task to load
// just for debugging, choose 1 example now
// task A 20 * 4 images + label
};
timeline.push(preload);

/* define welcome message trial */
var welcome = {
type: jsPsychHtmlKeyboardResponse,
stimulus: "<p style='font-size: 40px'>Welcome to the experiment.</p><p style='font-size: 30px'>Press any key to begin.</p>"
};
timeline.push(welcome);

/* define instructions trial */
var instructions = {
type: jsPsychHtmlKeyboardResponse,
stimulus: `
    <p>In this experiment, 4 images will appear on the screen. 3 out of 4 images were generated with a certain rule while one image (the odd one out) does not respect this rule. Select the odd one out by clicking on the image.</p>
    <p>Following your choice, you will be asked to rate how confident you were about your choice on a scale from 1 to 100. Then, you will receive feedback on the trial.</p>
    <p>For each rule you will perform 20 trials. You will be notified at each rule change. </p>
    <p> Press any button to continue </p>
    <div style='margin: auto; position: relative; width: 400px; height: 400px;'>
        <div style='position: absolute; top: 0;     left: 0; '><img src='../static/img/square.png'></img></div>
        <div style='position: absolute; top: 0;     right: 0;'><img src='../static/img/square.png'></img></div>
        <div style='position: absolute; bottom: 0;  left: 0; '><img src='../static/img/square.png'></img></div>
        <div style='position: absolute; bottom: 0;  right: 0;'><img src='../static/img/square.png'></img></div>
    </div>
`,
// <svg style='width: 40px; top: 0; left: 0;position: absolute;'viewBox="11.8 9 16 22" class="mouse"><path d="M20,21l4.5,8l-3.4,2l-4.6-8.1L12,29V9l16,12H20z"></path></svg>
// <script src="animate_mouse.js"></script> 

post_trial_gap: 2000
};

timeline.push(instructions);


// var multiple_choice = {
// type: jsPsychHtmlKeyboardResponse,
// stimulus: jsPsych.timelineVariable('stimulus'),
// choices: responses,
// prompt:"<p> Which image is different from the other three ?</p>",
// data: {
//     task: 'response',
//     correct_response: jsPsych.timelineVariable('correct_response')
// },
// extensions: [
//     {type: jsPsychExtensionMouseTracking, params: {}} //targets: ['#target']
// ],
// on_finish: function(data){
//     data.correct = jsPsych.pluginAPI.compareKeys(data.response, data.correct_response);
// }
// };

var multiple_choice = {
    // type: jsPsychHtmlKeyboardResponse,
    type: jsImageClick,
    // stimulus: jsPsych.timelineVariable('stimulus'),
    choices: jsPsych.timelineVariable('stimulus'),
    // choices: responses,
    // prompt:"<p> Which image is different from the other three ?</p>",
    data: {
        all_choices: jsPsych.timelineVariable('stimulus'),
        task: 'response',
        correct_response: jsPsych.timelineVariable('correct_response'),
        shuffled_array: jsPsych.timelineVariable('shuffled_array')
    },
    extensions: [
        {type: jsPsychExtensionMouseTracking, params: {}} //targets: ['#target']
    ],
    on_finish: function(data){
        data.correct = data.response == data.correct_response;
        // data.correct = jsPsych.pluginAPI.compareKeys(data.response, data.correct_response);
    }
};

var confidence = {
    type: jsPsychHtmlSliderResponse,
    stimulus: '<p>How different confident are you about your choice ?</p>',
    labels: ['0','100'],
    canvas_size: [200, 500],
    // prompt: '<p>How different confident are you about your choice ?</p>',
};

var feedback = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function(){
        
        var last_trial_data = jsPsych.data.get().last(2).values()[0];
        // var last_trial_correct = jsPsych.data.get().last(2).values()[0].correct;
        if(last_trial_data.correct){
            fb = "<h1 style='font-size: 60px; color: green;'>Correct!</h1>";
        } else {
            fb = "<h1 style='font-size: 60px; color: red'>Wrong</h1>";
        }
        
        extra_class = []
        for(let i = 0; i<4;i++){
            if(i == last_trial_data.correct_response){extra_class.push('correct-choice')}
            else if(i == last_trial_data.response && i != last_trial_data.correct_response){extra_class.push('wrong-choice')}
            else{extra_class.push('')}
        }
        // <div id='jspsych-image' style='position: relative; width: 750px; height: 750px;'>
        container_size = 80
        div_size = container_size * 35 / 100
        
        html = 
        `
        <div id='jspsych-image' style='position: relative; width: min(80vw, 80vh); height: min(80vw, 80vh);'>
                
                <div style='position: absolute; top: 40%; left: 30%; bottom: 40%; right: 30%;'>${fb}</div>
                
                <div class='jspsych-image' id='jspsych-image-0' data-choice='0' style='top: 0;     left: 0;'><img style="max-width: 100%; max-height: 100%;" src='${last_trial_data.all_choices[0]}' class='${extra_class[0]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-1' data-choice='1' style='top: 0;     right: 0;'><img style="max-width: 100%; max-height: 100%;" src='${last_trial_data.all_choices[1]}' class='${extra_class[1]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-2' data-choice='2' style='bottom: 0;  left: 0;'><img style="max-width: 100%; max-height: 100%;" src='${last_trial_data.all_choices[2]}' class='${extra_class[2]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-3' data-choice='3' style='bottom: 0;  right: 0;'><img style="max-width: 100%; max-height: 100%;" src='${last_trial_data.all_choices[3]}' class='${extra_class[3]}'></img></div>

        </div>`
        return html
        
        // if(last_trial_correct){
        //   return "<h1 style='fontsize: 60px; color: green;'>Correct!</h1>";
        // } else {
        //   return "<h1 style='fontsize: 60px; color: red'>Wrong.</h1>";
        // }
        
    },

    choices: "NO_KEYS",
    // trial_duration: 2500,
    trial_duration: function(){if(jsPsych.data.get().last(2).values()[0].correct){return 1500} else {return 2500}},    
};

var new_rule = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: "<h1 style='font-size: 60px'>New Rule!</h1> <p>Press any key to begin.</p>"
};

for (let i = 0; i < tasks.length; i++) {
    /* define test procedure */
    var block = {
        // timeline: [fixation, multiple_choice, confidence, feedback],
        timeline: [multiple_choice, confidence, feedback],
        timeline_variables: all_test_stimuli[i],
    };

    timeline.push(new_rule);
    timeline.push(block);

}




// /* define test procedure */
// var block_set = {
//     // timeline: [fixation, multiple_choice, confidence, feedback],
//     timeline: [welcome, block],
//     timeline_variables: all_tasks,
// };
// timeline.push(block_set);

/* define debrief */
var debrief_block = {
type: jsPsychHtmlKeyboardResponse,
stimulus: function() {

    var trials = jsPsych.data.get().filter({task: 'response'});
    var correct_trials = trials.filter({correct: true});
    var accuracy = Math.round(correct_trials.count() / trials.count() * 100);
    var rt = Math.round(correct_trials.select('rt').mean());

    return `<p>You responded correctly on ${accuracy}% of the trials.</p>
    <p>Your average response time was ${rt}ms.</p>
    <p>Press any key to complete the experiment. Thank you!</p>`;

}
};
timeline.push(debrief_block);

/* start the experiment */
jsPsych.run(timeline);
  