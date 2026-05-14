// ───────────────── SHOW FILE NAME ─────────────────

function handleFile(input){

    const file = input.files[0];

    if(file){

        document.getElementById('fileName').style.display = 'block';

        document.getElementById('fileNameText').innerText = file.name;
    }
}


// ───────────────── ANALYZE RESUME ─────────────────

async function analyzeResume(){

    const fileInput = document.getElementById('resumeFile');

    const role = document.getElementById('jobRole').value;

    if(fileInput.files.length === 0){

        alert('Please upload a PDF resume.');

        return;
    }

    const formData = new FormData();

    formData.append(
        'resume',
        fileInput.files[0]
    );

    formData.append(
        'role',
        role
    );

    try{

        const response = await fetch('/analyze',{

            method:'POST',

            body:formData

        });

        const data = await response.json();

        // ERROR HANDLING
        if(data.error){

            alert(data.error);

            return;
        }

        // SHOW RESULT CARD
        document.getElementById('resultCard').style.display = 'block';

        // SCORE
        document.getElementById('scoreNum').innerText =
            data.ats_score;

        // SCORE MESSAGE
        let message = '';

        if(data.ats_score >= 80){

            message = 'Excellent ATS compatibility.';

        }else if(data.ats_score >= 60){

            message = 'Good resume but can be improved.';

        }else{

            message = 'Low ATS score. Add more relevant skills.';
        }

        document.getElementById('scoreMsg').innerText =
            message;

        // ROLE
        document.getElementById('roleLabel').innerText =
            data.role;

        document.getElementById('missingRole').innerText =
            data.role;

        // BASIC INFO
        document.getElementById('candidateName').innerText =
            data.name;

        document.getElementById('email').innerText =
            data.email;

        document.getElementById('phone').innerText =
            data.phone;

        document.getElementById('wordCount').innerText =
            data.word_count;

        // SKILLS FOUND
        displayTags(
            'skillsFound',
            data.skills_found
        );

        // MATCHED SKILLS
        displayTags(
            'matchedSkills',
            data.matched_skills
        );

        // MISSING SKILLS
        displayTags(
            'skillsMissing',
            data.missing_skills
        );

        // SUGGESTIONS
        const suggestionsList =
            document.getElementById('suggestionsList');

        suggestionsList.innerHTML = '';

        data.suggestions.forEach(item => {

            const li = document.createElement('li');

            li.innerText = item;

            suggestionsList.appendChild(li);

        });

        // SCROLL TO RESULT
        document.getElementById('resultCard')
            .scrollIntoView({
                behavior:'smooth'
            });

    }catch(error){

        console.error(error);

        alert('Something went wrong.');

    }

}


// ───────────────── DISPLAY TAGS ─────────────────

function displayTags(containerId, items){

    const container = document.getElementById(containerId);

    container.innerHTML = '';

    if(items.length === 0){

        container.innerHTML = '<p>No data found</p>';

        return;
    }

    items.forEach(item => {

        const tag = document.createElement('span');

        tag.innerText = item;

        container.appendChild(tag);

    });

}