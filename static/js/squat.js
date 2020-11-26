window.onload = function() {
// More API functions here:
        // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose

        // the link to your model provided by Teachable Machine export panel
        const URL = "../static/exercise_model/squat-model/";
        let model, webcam, ctx, labelContainer, maxPredictions;

        let buttonStart, buttonStop;
        let is_playing = false;
        let status = "stand";
        let count = 0;
        let countNum = document.querySelector('.counter-num-in');
        let countRange = document.querySelector('.counter-range-in');
        let countAudio = 0;
        let audio = null;
        let is_exercise = null;
        // let audio = new Audio('audio_file.mp3');
        // audio.play();

        buttonStart = document.querySelector('.button-start');
        buttonStart.addEventListener('click', function(){
            init();
            is_playing = true;

            fetch('http://localhost:5000/squat-start', {mode:'no-cors'})
            .then((res) => {
                res.text();
            })
            .then((data) => {
                console.log(data);
            }); 

            audio = new Audio('../static/audio/squat-start.mp3');
            audio.play();
            is_exercise = true;
        });

        buttonStop = document.querySelector('.button-stop');
        buttonStop.addEventListener('click', function(){
            is_playing = false;
            count = 0;
            countNum.innerHTML = count.toString() + " 회";
            countRange.value = count;

            fetch('http://localhost:5000/stop-all', {mode:'no-cors'})
            .then((res) => {
                res.text();
            })
            .then((data) => {
                console.log(data);
            }); 

            countAudio = 0;
            audio = new Audio('../static/audio/squat-stop.mp3');
            audio.play();
            is_exercise = false;
        });


        async function init() {
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";

            // load the model and metadata
            // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
            // Note: the pose library adds a tmPose object to your window (window.tmPose)
            model = await tmPose.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();

            // Convenience function to setup a webcam
            const size = 200;
            const flip = true; // whether to flip the webcam
            webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
            await webcam.setup(); // request access to the webcam
            await webcam.play();
            window.requestAnimationFrame(loop);

            // append/get elements to the DOM
            const canvas = document.getElementById("canvas");
            canvas.width = size;
            canvas.height = size;
            ctx = canvas.getContext("2d");
            labelContainer = document.getElementById("label-container");
            for (let i = 0; i < maxPredictions; i++) { // and class labels
                labelContainer.appendChild(document.createElement("div"));
            }
        }

        async function loop(timestamp) {
            webcam.update(); // update the webcam frame
            await predict();
            window.requestAnimationFrame(loop);
        }

        
        async function predict() {
            // Prediction #1: run input through posenet
            // estimatePose can take in an image, video or canvas html element
            const {
                pose,
                posenetOutput
            } = await model.estimatePose(webcam.canvas);
            // Prediction 2: run input through teachable machine classification model
            const prediction = await model.predict(posenetOutput);

            // count exercise
            if(prediction[0].probability.toFixed(2) > 0.95) {
                if(status == "squat") {
                    count++;
                    countNum.innerHTML = count.toString() + " 회";
                    countRange.value = count % 10 ;

                    if(is_exercise == true) {
                        fetch('http://localhost:5000/led?count=' + (count % 10), {mode:'no-cors'})
                        .then((res) => {
                            res.text();
                        })
                        .then((data) => {
                            console.log(data);
                        }); 
                    }

                    countAudio++;
                    audio = new Audio( "../static/audio/" + (countAudio % 10) + ".mp3" );
                    audio.play();

                    
                }
                status = "stand";
            }
            else if(prediction[1].probability.toFixed(2) > 0.95) {
                
                status = "squat";
            }
            else if(prediction[2].probability.toFixed(2) > 0.95) {
                if(status != "bent") {
                    
                    if(is_exercise == true) {
                        fetch('http://localhost:5000/wrong-pose', {mode:'no-cors'})
                        .then((res) => {
                            res.text();
                        })
                        .then((data) => {
                            console.log(data);
                        });     
                    }
                  
                    audio = new Audio( "../static/audio/squat-wrongpose.mp3" );
                    audio.play();
                }

                status = "bent";
            }

            for (let i = 0; i < maxPredictions; i++) {
                const classPrediction =
                    prediction[i].className + ": " + prediction[i].probability.toFixed(2);
                labelContainer.childNodes[i].innerHTML = classPrediction;
            }

            // finally draw the poses
            drawPose(pose);
        }

        function drawPose(pose) {
            if (webcam.canvas) {
                ctx.drawImage(webcam.canvas, 0, 0);
                // draw the keypoints and skeleton
                if (pose) {
                    const minPartConfidence = 0.5;
                    tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
                    tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
                }
            }
        }
};
