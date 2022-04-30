
// Define global variables.
var low_quality = false;

function verify_unload(e){
    e.preventDefault();
    (e || window.event).returnValue = null;
    return null;
};
window.addEventListener("beforeunload", verify_unload);


disard_exp = () => {discard_experiment("{{workerId}}", "{{assignmentId}}", "{{hitId}}", "{{code_reject}}")}

$(window).on('unload', disard_exp);


/* initialize jsPsych */
var jsPsych = initJsPsych({
    show_progress_bar: true,
    auto_update_progress_bar: false,

on_finish: function() {
    // jsPsych.data.displayData();

    // Remove requirement to verify redirect
    window.removeEventListener("beforeunload", verify_unload);
    $(window).off('unload', disard_exp);

    // Add interactions to the data variable
    var interaction_data = jsPsych.data.getInteractionData();
    jsPsych.data.get().addToLast({interactions: interaction_data.json()});

    // Display jsPsych data in viewport.
    // jsPsych.data.displayData();
    
    // calculate the number of correct responses to the instruction question
    var n_failed_comp_checks = jsPsych.data.get().filter({trial_type: "survey-multi-select"}).count()-1;
    // the number of wrongly answered catch_trials
    var n_failed_att_checks = jsPsych.data.get().filter({catch_trial: true}).filter({correct: false}).count();
    // var n_failed_comp_checks = jsPsych.data.get().select('trial_type').subset(function(x){ return x == "survey-multi-select"; }).count()-1;
    
    // rule descriptions aren't empty
    var n_empty_rule_desc = jsPsych.data.get().filter({catch_trial: true}).filter({correct: false}).count();
    
    // reaction times aren't too low
    var n_rt_below_thres = jsPsych.data.get().filter({catch_trial: true}).filter({correct: false}).count();

    var low_quality = n_failed_att_checks>2;

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
];


function load_task(baseFolder, task, n_trials_){
    var all_images = [];
    // var preload_images = [];
    for (let i = 0; i < n_trials_; i++) {
        var taskFolder = baseFolder + task + '/'
        
        all_images.push([
            taskFolder + pad(i, 2) + '_' + 0 + '.png', 
            taskFolder + pad(i, 2) + '_' + 1 + '.png', 
            taskFolder + pad(i, 2) + '_' + 2 + '.png', 
            taskFolder + pad(i, 2) + '_' + 3 + '.png'
        ]);
    }
    return all_images
}


var all_preload_images = []
var all_tasks_images = []

var practice_images = load_task(baseFolder, 'practice_img', 3)
var preload_images = [].concat.apply([], practice_images)
// all_preload_images.push(preload_images)
var preload_practice = preload_images

for (let i = 0; i < n_tasks; i++) {
    var images = load_task(baseFolder, tasks[i], n_trials)
    var preload_images = [].concat.apply([], images)
    all_tasks_images.push(images)
    all_preload_images.push(preload_images)
}


// var preload_images = [].concat.apply([], all_preload_images)

/* define trial stimuli array for timeline variables */

var labelArray = [0,1,2,3];

var practice_stimuli = [];
for (let i = 0; i < 3; i++) {

    var shuffledArray = jsPsych.randomization.shuffleNoRepeats(labelArray);
    var images = []
    for (let j = 0; j < 4; j++){
        if(shuffledArray[j] == 3){var indexCorrect=j;}
        images.push(practice_images[i][shuffledArray[j]])
    }
    practice_stimuli.push({
        // stimulus: all_images[i],
        stimulus: images,
        correct_response: indexCorrect,
        shuffled_array: shuffledArray,
        catch_trial: false,
        n_trials: 3,
    })
}

var stim_trial_idx = [];

for (var i = 0; i < n_trials; i++) {
    stim_trial_idx.push(i);
}

var all_test_stimuli = []

for (let k = 0; k < n_tasks; k++) {

    var catch_trial_index = Math.floor(Math.random() * 10) + 5;
    var test_stimuli = [];
    
    var stim_order = jsPsych.randomization.shuffleNoRepeats(stim_trial_idx);
    
    for (let i = 0; i < n_trials; i++) {
        
        var shuffledArray = jsPsych.randomization.shuffleNoRepeats(labelArray);
        var images = []
        for (let j = 0; j < 4; j++){
            if(shuffledArray[j] == 3){var indexCorrect=j;}
            images.push(all_tasks_images[k][stim_order[i]][shuffledArray[j]])
        }

        test_stimuli.push({
            stim_idx: stim_order[i],
            stimulus: images,
            correct_response: indexCorrect,
            shuffled_array: shuffledArray,
            catch_trial: false,
            n_trials: n_trials+1,
        })

        // adds a catch trial
        if(i == catch_trial_index){
            test_stimuli.push({
                // stimulus: all_images[i],
                stim_idx: stim_order[i],
                stimulus: images,
                correct_response: indexCorrect,
                shuffled_array: shuffledArray,
                catch_trial: true,
                n_trials: n_trials+1,
            })
        }

    }
    all_test_stimuli.push(test_stimuli)
}

var n_all_trials = n_trials * n_tasks + 3


// preload_practice
// var preload = {
// type: jsPsychPreload,
// images: preload_images
// };
// timeline.push(preload);

/* define welcome message trial */
var welcome = {
type: jsPsychHtmlKeyboardResponse,
stimulus: "<p style='font-size: 40px'>Welcome to the experiment.</p><p style='font-size: 30px'>Press any key to begin.</p>"
};
timeline.push(welcome);

/* define instructions trial */
var instructions_1 = {
type: jsPsychHtmlKeyboardResponse,
stimulus: `
        <p>This experiment aims to measure humans' visual reasoning skills. You will go through a practice session consisting of 3 trials, followed by 6 blocks of 21 trials.</p>
        
        <p>When presented with a square with a cross in the middle of the screen, place your cursor on it to start the trial.</p>

        <p>Press any button to continue</p>
        <div style="font-size:60px; border: 5px solid black; width: 60px; height: 60px; margin: 0 auto; text-align: center; display: flex; justify-content: center; align-items: center;"> + </div>
    `,
    // post_trial_gap: 1000
};

var instructions_2 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
        <p>4 images will appear on the screen. 3 out of 4 images were generated with a certain rule while one image (the odd one out) does not respect this rule.</p>
        <p>Select the odd one out by clicking on the image.</p>
            
        <p>Press any button to continue</p>
        <div style='margin: auto; position: relative; width: 400px; height: 400px;'>
            <div style='position: absolute; top: 0;     left: 0; width: 30%; height: 30%;'><img style='width: 100%; height: 100%;' src='../static/human_exp_images/practice_img/00_0.png'></img></div>
            <div style='position: absolute; top: 0;     right: 0;width: 30%; height: 30%;'><img style='width: 100%; height: 100%;' src='../static/human_exp_images/practice_img/00_1.png'></img></div>
            <div style='position: absolute; bottom: 0;  left: 0; width: 30%; height: 30%;'><img style='width: 100%; height: 100%;' src='../static/human_exp_images/practice_img/00_2.png'></img></div>
            <div style='position: absolute; bottom: 0;  right: 0;width: 30%; height: 30%;'><img style='width: 100%; height: 100%; border: 4px solid green;' src='../static/human_exp_images/practice_img/00_3.png'></img></div>
        </div>
    `,
    // post_trial_gap: 2000
};

var instructions_3 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
        <p>Following your choice, you will be asked to rate how confident you were about your choice on a scale from 0 to 100. Then, you will receive feedback on the trial.</p>
        
        <p>The 21 trials of a block use the same rule and each block uses a different rule. At the end of each block, you will asked to describe the rule before starting a new block.</p>
        <p>Please do not take breaks only in between blocks not in between trials.</p>
        <p>The following 3 trials will allow you to get familiar with the odd-one-out task. The experiment starts after this practice session.</p>
        
        <p>Press any button to continue</p>
        <div style='margin: auto; position: relative; width: 400px; height: 400px;'>
        <input type="range" class="jspsych-slider" value="50" min="0" max="100" step="1" id="jspsych-html-slider-response-response"></input>
        <div style="border: 1px solid transparent; display: inline-block; position: absolute; left:-50%; text-align: center; width:100%;">
            <span style="text-align: center; font-size: 80%;">0</span> 
        </div>
        <div style="border: 1px solid transparent; display: inline-block; position: absolute; left:50%; text-align: center; width:100%;">
            <span style="text-align: center; font-size: 80%;">100</span> 
        </div>
        </div>
        
        `,
    // post_trial_gap: 2000
};

var instructions_4 = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
        <p>The 21 trials of a block use the same rule and each block uses a different rule. At the end of each block, you will asked to describe the rule before starting a new block.</p>

        <p><b>This experiment requires the use of a mouse or a trackpad!</b> We ask you to please do not use the <b>BACK</b> or <b>REFRESH</b> buttons as they will terminate the experiment.</p>
        <p>We encourage taking brief pauses before the start or at the end of a each block. However, we urge you to avoid taking pauses during a block.</p>
        
        <p>The following 3 trials will allow you to get familiar with the odd-one-out task. The experiment starts after this practice session.</p>
        
        <p>Press any button to continue</p>
        `,
    // post_trial_gap: 2000
};


timeline.push(instructions_1);
timeline.push(instructions_2);
timeline.push(instructions_3);
timeline.push(instructions_4);

var instruction_check = {
    type: jsPsychSurveyMultiSelect,
    questions: [
        {
            type: 'multi-select',
            prompt: "Select the correct answers. In this experiment:", 
            name: 'Instruction Check', 
            options: [
                    "No mouse or trackpad are needed.", 
                    "The practice session contains as many trials as the other blocks.", 
                    "There are 6 blocks of 21 trials.", 
                    "It's ok to take breaks within a block.", 
                    "The tasks consists of choosing one image that's different from the other three.",
                    "It's possible to reload the page in between trials."
                ], 
            required: true,
        }
    ],
  };

timeline.push(instruction_check);

var instruction_error = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `
    <h1> Please read the instructions carefully!</h1>
    
        <p>This experiment aims to measure humans' visual reasoning skills. You will go through a practice session consisting of 3 trials, followed by 6 blocks of 21 trials.</p>
        
        <p>When presented with a square with a cross in the middle of the screen, place your cursor on it to start the trial.</p>
        <p>4 images will appear on the screen. 3 out of 4 images were generated with a certain rule while one image (the odd one out) does not respect this rule.</p>
        <p>Select the odd one out by clicking on the image.</p>
        <p>Following your choice, you will be asked to rate how confident you were about your choice on a scale from 0 to 100. Then, you will receive feedback on the trial.</p>
        
        <p>The 21 trials of a block use the same rule and each block uses a different rule. At the end of each block, you will asked to describe the rule before starting a new block.</p>
        
        <p><b>This experiment requires the use of a mouse or a trackpad!</b> We ask you to please do not use the <b>BACK</b> or <b>REFRESH</b> buttons as they will terminate the experiment.</p>
        <p>We encourage taking brief pauses before the start/the end of a each block. However, we urge you to avoid taking pauses during a block.</p>

        <p>The following 3 trials will allow you to get familiar with the odd-one-out task. The experiment starts after this practice session.</p>
        
        <p>Press any button to continue</p>
        
    `,
    // post_trial_gap: 2000
};
// timeline.push(instruction_error);


var while_node = {
    timeline: [instruction_error, instruction_check],
    loop_function: function(data){
        var idx_loop = jsPsych.data.get().select('trial_type').subset(function(x){ return x == "survey-multi-select"; }).count();

        var data = jsPsych.data.get().last(1).values()[0].response['Instruction Check'];
        var correct_responses=[
            "There are 6 blocks of 21 trials.", 
            "The tasks consists of choosing one image that's different from the other three."
        ]
        var filteredArray = data.filter(function(n) {
            return correct_responses.indexOf(n) !== -1;
        });
        
        if( (idx_loop >= 5) || (data.length == 2 && filteredArray.length == 2)){
            return false;
        } else {
            return true;
        }
    }
}
// timeline.push(while_node);



var if_node = {
    timeline: [while_node],
    conditional_function: function(){
        var data = jsPsych.data.get().last(1).values()[0].response['Instruction Check'];
        var correct_responses=[
            "There are 6 blocks of 21 trials.", 
            "The tasks consists of choosing one image that's different from the other three."
        ]
        var filteredArray = data.filter(function(n) {
            return correct_responses.indexOf(n) !== -1;
        });
        
        if(data.length == 2 && filteredArray.length == 2){
            return false;
        } else {
            return true;
        }
    }
}
timeline.push(if_node);


var experiment_start = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: `<p style='font-size: 40px'>The practice session is over. The experiment begin now!</p> 
                <p>Please take pauses on only at the "new rule" pages.</p> 
                <p>Press any key to begin.</p>`
};

var new_rule = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: "<h1 style='font-size: 60px'>New Rule!</h1> <p>Press any key to begin.</p>"
};

var fixation = {
    // type: jsPsychHtmlKeyboardResponse,
    type: jsImageHover,
    // stimulus: '<div style=" width: 50%; height: 50%; position: absolute; top: 25%; left: 25%;"><div style="font-size:60px; border: 5px solid black; width: 100%; height: 100%; position: absolute; top: 0%; left: 0%; text-align: center; display: flex; justify-content: center; align-items: center;">+</div></div>',
    stimulus: '<div style="font-size:60px; border: 6px solid black;  width: 100%; height: 100%; position: absolute; top: calc(0% - 6px); left: calc(0% - 6px); text-align: center; display: flex; justify-content: center; align-items: center;">+</div>',
    // stimulus: `<img style="max-width: 100%; max-height: 100%;" src='../static/img/square.png'></img>`,
};

var multiple_choice = {
    type: jsImageClick,
    choices: jsPsych.timelineVariable('stimulus'),
    data: {
        all_choices: jsPsych.timelineVariable('stimulus'),
        task: 'response',
        document_dims: function(){return [document.body.clientWidth, document.body.clientHeight]},
        correct_response: jsPsych.timelineVariable('correct_response'),
        shuffled_array: jsPsych.timelineVariable('shuffled_array'),
        catch_trial: jsPsych.timelineVariable('catch_trial'),
    },
    extensions: [
        {type: jsPsychExtensionMouseTracking, params: {}} //targets: ['#target']
    ],
    // on_start: function(data){
    //     data.document_dims = [document.body.clientWidth, document.body.clientHeight]
    // },
    on_finish: function(data){
        data.correct = data.response == data.correct_response;
    }
};



// var confidence = {
//     type: jsPsychHtmlSliderResponse,
//     stimulus: '<p>How confident are you about your choice ?</p>',
//     labels: ['0','100'],
//     canvas_size: [200, 500],
// };

var confidence = {
    type: jsPsychHtmlHoverSlider,
    stimulus: '<p>How confident are you about your choice ? (click on the bar)</p>',
    labels: ['0','100'],
    canvas_size: [200, 500],
};

var feedback = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: function(){
        
        var last_trial_data = jsPsych.data.get().last(2).values()[0];
        if(last_trial_data.correct){
            // fb = "<h1 style='font-size: 60px; color: green;'>Correct!</h1>";
            fb = "<h1 style='font-size: 60px; color: green;'>Correct!</h1> <p>Press any key to continue.</p>";
        } else {
            // fb = "<h1 style='font-size: 60px; color: red'>Wrong</h1>";
            fb = "<h1 style='font-size: 60px; color: red'>Wrong</h1> <p>Press any key to continue.</p>";
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
                
                <div class='jspsych-image' id='jspsych-image-0' data-choice='0' style='top: 0;     left: 0;'><img style="width: 100%; height: 100%;" src='${last_trial_data.all_choices[0]}' class='${extra_class[0]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-1' data-choice='1' style='top: 0;     right: 0;'><img style="width: 100%; height: 100%;" src='${last_trial_data.all_choices[1]}' class='${extra_class[1]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-2' data-choice='2' style='bottom: 0;  left: 0;'><img style="width: 100%; height: 100%;" src='${last_trial_data.all_choices[2]}' class='${extra_class[2]}'></img></div>
                <div class='jspsych-image' id='jspsych-image-3' data-choice='3' style='bottom: 0;  right: 0;'><img style="width: 100%; height: 100%;" src='${last_trial_data.all_choices[3]}' class='${extra_class[3]}'></img></div>

        </div>`
        return html
        
    },

    // choices: "NO_KEYS",
    // trial_duration: 2500,
    // trial_duration: function(){if(jsPsych.data.get().last(2).values()[0].correct){return 1500} else {return 2500}},

    on_finish: function() {
        var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
        jsPsych.setProgressBar( curr_progress_bar_value + (1/n_all_trials) );
    }

};

var task_description = {
    type: jsPsychSurveyText,
    questions: [
      {prompt: 'Describe the rule in a few words.', rows: 5}
    ]
}


var preload = {
    type: jsPsychPreload,
    images: preload_practice

};

var practice_block = {
    // timeline: [fixation, multiple_choice, confidence, feedback],
    timeline: [fixation, multiple_choice, confidence, feedback],
    timeline_variables: practice_stimuli,
    on_timeline_finish: function() {
        console.log('This timeline has finished.');
        save_block(jsPsych.data.get().last(4 * practice_stimuli.length).json())        
    },
};


timeline.push(preload);
timeline.push(practice_block);
timeline.push(experiment_start);

for (let i = 0; i < tasks.length; i++) {
    
    var preload = {
        type: jsPsychPreload,
        images: all_preload_images[i],
        // on_start: function() {
        //     // set progress bar to 0 at the start of experiment
        //     jsPsych.setProgressBar(0);
        // }
    };
    
    var block_end = {
        type: jsPsychHtmlKeyboardResponse,
        stimulus: "<h1 style='font-size: 60px'>Block End</h1>",
        choices: "NO_KEYS",
        trial_duration: 500,
        on_start: function(){
            save_block(jsPsych.data.get().last(1 + 4 * all_test_stimuli[i].length).json());
            console.log('saved block');
        },
        
    };
    
    /* define test procedure */
    var block = {
        // timeline: [fixation, multiple_choice, confidence, feedback],
        timeline: [fixation, multiple_choice, confidence, feedback],
        timeline_variables: all_test_stimuli[i],
        // on_timeline_finish: function() {
        //     console.log('This timeline has finished.');
        //     save_block(jsPsych.data.get().last(1 + 4 * all_test_stimuli[i].length).json())        
        // },
    };
    
    timeline.push(preload);
    timeline.push(new_rule);
    timeline.push(block);
    timeline.push(task_description);
    timeline.push(block_end);
    
}

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
  
// }
