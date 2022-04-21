var jsImageClick = (function (jspsych) {
  'use strict';

  const info = {
      name: "image-click",
      parameters: {
          /** The HTML string to be displayed */
        //   stimulus: {
        //       type: jspsych.ParameterType.HTML_STRING,
        //       pretty_name: "Stimulus",
        //       default: undefined,
        //   },
        //   /** Array containing the label(s) for the button(s). */
          choices: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Choices",
              default: undefined,
              array: true,
          },
        //   /** The HTML for creating button. Can create own style. Use the "%choice%" string to indicate where the label from the choices parameter should be inserted. */
        //   button_html: {
        //       type: jspsych.ParameterType.HTML_STRING,
        //       pretty_name: "Button HTML",
        //       default: '<button class="jspsych-btn">%choice%</button>',
        //       array: true,
        //   },
          /** Any content here will be displayed under the button(s). */
          prompt: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Prompt",
              default: null,
          },
          /** How long to show the stimulus. */
          stimulus_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Stimulus duration",
              default: null,
          },
          /** How long to show the trial. */
          trial_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Trial duration",
              default: null,
          },
          /** The vertical margin of the button. */
          margin_vertical: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Margin vertical",
              default: "0px",
          },
          /** The horizontal margin of the button. */
          margin_horizontal: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Margin horizontal",
              default: "8px",
          },
          /** If true, then trial will end when user responds. */
          response_ends_trial: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Response ends trial",
              default: true,
          },
      },
  };

  class ImageClickPlugin {
      constructor(jsPsych) {
          this.jsPsych = jsPsych;
      }
      trial(display_element, trial) {
          // display stimulus
        //   var html = '<div id="jspsych-html-button-response-stimulus">' + trial.stimulus + "</div>";
        //   var html = '<div id="jspsych-image-click">' + trial.stimulus + "</div>";
        // style: "max-width=100%; max-height: 100%;" 
        //display buttons
        var html = ` <div id='jspsych-image-click-button' style='position: relative;  width: min(80vw, 80vh); height: min(80vw, 80vh);'>
                <div class='jspsych-image-click-button' id='jspsych-image-click-button-0' data-choice='0' style='top: 0;     left: 0;'> <img style="width: 100%; height: 100%;" src='${trial.choices[0]}'></img></div>
                <div class='jspsych-image-click-button' id='jspsych-image-click-button-1' data-choice='1' style='top: 0;     right: 0;'><img style="width: 100%; height: 100%;" src='${trial.choices[1]}'></img></div>
                <div class='jspsych-image-click-button' id='jspsych-image-click-button-2' data-choice='2' style='bottom: 0;  left: 0;'> <img style="width: 100%; height: 100%;" src='${trial.choices[2]}'></img></div>
                <div class='jspsych-image-click-button' id='jspsych-image-click-button-3' data-choice='3' style='bottom: 0;  right: 0;'><img style="width: 100%; height: 100%;" src='${trial.choices[3]}'></img></div>
            </div>`

        //   var buttons = [];
        //   if (Array.isArray(trial.button_html)) {
        //       if (trial.button_html.length == trial.choices.length) {
        //           buttons = trial.button_html;
        //       }
        //       else {
        //           console.error("Error in html-button-response plugin. The length of the button_html array does not equal the length of the choices array");
        //       }
        //   }
        //   else {
        //       for (var i = 0; i < trial.choices.length; i++) {
        //           buttons.push(trial.button_html);
        //       }
        //   }

        // html += '<div id="jspsych-html-button-response-btngroup">';
        //   for (var i = 0; i < trial.choices.length; i++) {
        //       var str = buttons[i].replace(/%choice%/g, trial.choices[i]);
        //       html +=
        //           '<div class="jspsych-html-button-response-button" style="display: inline-block;" id="jspsych-html-button-response-button-' + i +
        //               '" data-choice="' +
        //               i +
        //               '">' +
        //               str +
        //               "</div>";
        //   }
          
        //   html += "</div>";

          //show prompt if there is one
          if (trial.prompt !== null) {
              html += trial.prompt;
          }
          display_element.innerHTML = html;
          // start time
          var start_time = performance.now();
          // add event listeners to buttons
          for (var i = 0; i < trial.choices.length; i++) {
              display_element
                  .querySelector("#jspsych-image-click-button-" + i)
                  .addEventListener("click", (e) => {
                  var btn_el = e.currentTarget;
                  var choice = btn_el.getAttribute("data-choice"); // don't use dataset for jsdom compatibility
                  after_response(choice);
              });
          }
          // store response
          var response = {
              rt: null,
              button: null,
          };
          // function to end trial when it is time
          const end_trial = () => {
              // kill any remaining setTimeout handlers
              this.jsPsych.pluginAPI.clearAllTimeouts();
              // gather the data to store for the trial
              var trial_data = {
                  rt: response.rt,
                  stimulus: trial.stimulus,
                  response: response.button,
              };
              // clear the display
              display_element.innerHTML = "";
              // move on to the next trial
              this.jsPsych.finishTrial(trial_data);
          };
          // function to handle responses by the subject
          function after_response(choice) {
              // measure rt
              var end_time = performance.now();
              var rt = Math.round(end_time - start_time);
              response.button = parseInt(choice);
              response.rt = rt;
              // after a valid response, the stimulus will have the CSS class 'responded'
              // which can be used to provide visual feedback that a response was recorded
              display_element.querySelector("#jspsych-image-click-button-" + choice).className +=
                  " responded";
              // disable all the buttons after a response

            // might be useful but won't use it for now
            
            //   var btns = document.querySelectorAll(".jspsych-image-click-button button");
            //   for (var i = 0; i < btns.length; i++) {
            //       //btns[i].removeEventListener('click');
            //       btns[i].setAttribute("disabled", "disabled");
            //   }
              if (trial.response_ends_trial) {
                  end_trial();
              }
          }
          // hide image if timing is set
          if (trial.stimulus_duration !== null) {
              this.jsPsych.pluginAPI.setTimeout(() => {
                  display_element.querySelector("#jspsych-image-click-button").style.visibility = "hidden";
              }, trial.stimulus_duration);
          }
          // end trial if time limit is set
          if (trial.trial_duration !== null) {
              this.jsPsych.pluginAPI.setTimeout(end_trial, trial.trial_duration);
          }
      }
      simulate(trial, simulation_mode, simulation_options, load_callback) {
          if (simulation_mode == "data-only") {
              load_callback();
              this.simulate_data_only(trial, simulation_options);
          }
          if (simulation_mode == "visual") {
              this.simulate_visual(trial, simulation_options, load_callback);
          }
      }
      create_simulation_data(trial, simulation_options) {
          const default_data = {
              stimulus: trial.stimulus,
              rt: this.jsPsych.randomization.sampleExGaussian(500, 50, 1 / 150, true),
              response: this.jsPsych.randomization.randomInt(0, trial.choices.length - 1),
          };
          const data = this.jsPsych.pluginAPI.mergeSimulationData(default_data, simulation_options);
          this.jsPsych.pluginAPI.ensureSimulationDataConsistency(trial, data);
          return data;
      }
      simulate_data_only(trial, simulation_options) {
          const data = this.create_simulation_data(trial, simulation_options);
          this.jsPsych.finishTrial(data);
      }
      simulate_visual(trial, simulation_options, load_callback) {
          const data = this.create_simulation_data(trial, simulation_options);
          const display_element = this.jsPsych.getDisplayElement();
          this.trial(display_element, trial);
          load_callback();
          if (data.rt !== null) {
              this.jsPsych.pluginAPI.clickTarget(display_element.querySelector(`div[data-choice="${data.response}"] button`), data.rt);
          }
      }
  }
  ImageClickPlugin.info = info;

  return ImageClickPlugin;

})(jsPsychModule);
