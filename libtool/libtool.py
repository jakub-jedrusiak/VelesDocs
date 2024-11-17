from shutil import copyfile
from os.path import exists
import velesresearch as vls

defaultOptions = {"isRequired": True, "autocomplete": "off"}

commaValidator = vls.regexValidator(
    r"^(\d+, ?)*\d+$",
    'Use comma separated values, e.g. "1, 3, 5".',
)

categories = """Mental Health and Disorders
Personality and Traits
Cognitive and Behavioral Assessments
Social and Interpersonal Factors
Motivation and Achievement
Well-Being and Quality of Life
Developmental and Educational Psychology
Health Psychology
Clinical Assessments
Emotional and Affective States
Social Cognition and Attitudes
Occupational and Organizational Psychology
Ethical and Moral Constructs""".split(
    "\n"
)

subcategories = """Depression
Anxiety
Stress
Post-Traumatic Stress Disorder (PTSD)
Bipolar Disorder
Schizophrenia
Obsessive-Compulsive Disorder (OCD)
Eating Disorders

Big Five Personality Traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
Emotional Intelligence
Narcissism
Self-Esteem
Resilience

Attention
Memory
Executive Function
Problem-Solving
Impulsivity

Social Anxiety
Relationship Satisfaction
Attachment Styles
Empathy
Conflict Resolution

Academic Motivation
Work Motivation
Grit and Perseverance
Goal Orientation

Life Satisfaction
Happiness
Mindfulness
Subjective Well-Being
Burnout

Child Development
Adolescent Psychology
Learning Styles
Cognitive Development

Coping Mechanisms
Sleep Quality
Substance Use
Eating Habits
Chronic Illness Impact

Diagnostic Tools
Risk Assessment
Symptom Checklists

Positive and Negative Affect
Mood States
Anger
Fear

Prejudice and Bias
Social Desirability
Group Dynamics
Trust

Job Satisfaction
Leadership Styles
Organizational Commitment
Work-Life Balance

Moral Reasoning
Values and Beliefs
Altruism""".split(
    "\n\n"
)

subcategories = [x.split("\n") for x in subcategories]

subcategories_answers = []
for index, category in enumerate(categories):
    for subcategory in subcategories[index]:
        subcategories_answers.append(
            {
                "text": subcategory,
                "visibleIf": f"{{grand_categories}} contains '{category}'",
            }
        )

form = vls.page(
    "libtool",
    vls.text(
        "name",
        "Questionnaire's name",
        placeholder="Ten Item Personality Inventory",
        **defaultOptions,
    ),
    vls.text(
        "abbreviation", "Name's abbreviation", placeholder="TIPI", **defaultOptions
    ),
    vls.text(
        "language",
        "Language code",
        description="The 2-letter ISO 639-1 language code. See <a href='https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes' target='_blank' rel='noopener noreferrer'>Wikipedia</a> for the full list.",
        placeholder="en",
        validators=vls.regexValidator(
            "^[a-z]{2}$", "Write a correct 2-letter language code"
        ),
        **defaultOptions,
    ),
    vls.textLong(
        "description",
        "Description",
        description="A short 2-3 sentences description of the questionnaire.",
        **defaultOptions,
    ),
    vls.dropdownMultiple(
        "grand_categories",
        "Grand categories",
        categories,
        description="Select all that apply.",
        **defaultOptions,
    ),
    vls.dropdownMultiple(
        "subcategories",
        "Subcategories",
        subcategories_answers,
        description="Select all that apply.",
        **defaultOptions | {"isRequired": False},
    ),
    vls.textLong(
        "original",
        "The ZBib APA citation of the original questionnaire",
        description="Go to <a href='https://zbib.org' target='_blank' rel='noopener noreferrer'>zbib.org</a> and add the original article (or all of them). Set the style to APA 7. Copy HTML (the arrow next to the Copy to Clipboard button) and paste it here.",
        **defaultOptions,
    ),
    vls.yesno(
        "isAdaptation",
        "Is this test an adaptation?",
        description="i.e. is this version of the test described in a different article than the original questionnaire?",
        **defaultOptions,
    ),
    vls.textLong(
        "adaptation",
        "The ZBib APA citation of the adaptation",
        description="Go to <a href='https://zbib.org' target='_blank' rel='noopener noreferrer'>zbib.org</a> and add the adaptation article (or all of them). Set the style to APA 7. Copy HTML (the arrow next to the Copy to Clipboard button) and paste it here.",
        **defaultOptions,
        visibleIf="{isAdaptation}",
    ),
    vls.yesno("hasSubscales", "Does this test have subscales?", **defaultOptions),
    vls.matrixDynamic(
        "subscales",
        "Subscales",
        vls.text("name", "Name", **defaultOptions),
        vls.text(
            "items", "Items' numbers", validators=commaValidator, **defaultOptions
        ),
        vls.text(
            "reliability",
            "Reliability (Cronbach's alpha)",
            inputType="number",
            min=0.00,
            max=1.00,
            step="0.01",
            **defaultOptions,
        ),
        description="Write the name of the subscale and the numbers of the items that belong to it. Separate the items with commas. Write the Cronbach's alpha reliability coefficient as a number (e.g. 0.85).",
        visibleIf="{hasSubscales}",
        minRowCount=2,
    ),
    vls.text(
        "reliability",
        "Overall reliability (Cronbach's alpha)",
        description="Write the Cronbach's alpha reliability coefficient as a number (e.g. 0.85). Use only if a singular score can be calculated for the whole questionnaire.",
        placeholder="0.85",
        inputType="number",
        min=0.00,
        max=1.00,
        step="0.01",
        requiredIf="{hasSubscales} = false",
        **defaultOptions | {"isRequired": False},
    ),
    vls.radio(
        "scoring",
        "Score calculation method",
        "A simple sum",
        "An average",
        showOtherItem=True,
        **defaultOptions,
    ),
    vls.yesno(
        "hasReverseItems", "Does this test have reverse scored items?", **defaultOptions
    ),
    vls.text(
        "reverse_items",
        "Reverse scored items",
        description="Comma-separated item numbers.",
        placeholder="2, 4, 6, 8, 10",
        validators=commaValidator,
        visibleIf="{hasReverseItems}",
        **defaultOptions,
    ),
    vls.matrixDynamic(
        "authors",
        "Implemented by",
        vls.text(
            "name", "Given name", **defaultOptions | {"autocomplete": "given-name"}
        ),
        vls.text(
            "surname", "Surname", **defaultOptions | {"autocomplete": "family-name"}
        ),
        vls.text(
            "affiliation",
            "Affiliation",
            **defaultOptions | {"autocomplete": "organization"},
        ),
        rowCount=1,
        minRowCount=1,
        description="Your name, surname, and affiliation.",
        **defaultOptions | {"autocomplete": None},
    ),
    vls.yesno(
        "specifyItems",
        "Do you want to specify the items and the scale here?",
        description="You can also do it directly in the generated Python code.",
        **defaultOptions,
    ),
    vls.textLong(
        "instruction",
        "Default instruction",
        description="Use HTML/CSS or markdown to style it.",
        visibleIf="{specifyItems}",
        **defaultOptions,
    ),
    vls.textLong("items", "Items", visibleIf="{specifyItems}", **defaultOptions),
    vls.radio(
        "items_separator",
        "Items' separator",
        [
            {"value": "\\n", "text": "New line"},
            {"value": ", ", "text": "Comma (with space)"},
            {"value": ",", "text": "Comma (without space)"},
            {"value": "; ", "text": "Semicolon (with space)"},
            {"value": ";", "text": "Semicolon (without space)"},
        ],
        showOtherItem=True,
        otherText="Custom",
        visibleIf="{specifyItems}",
        **defaultOptions,
    ),
    vls.textLong("scale", "Scale", visibleIf="{specifyItems}", **defaultOptions),
    vls.radio(
        "scale_separator",
        "Scale separator",
        [
            {"value": "\\n", "text": "New line"},
            {"value": ", ", "text": "Comma (with space)"},
            {"value": ",", "text": "Comma (without space)"},
            {"value": "; ", "text": "Semicolon (with space)"},
            {"value": ";", "text": "Semicolon (without space)"},
        ],
        showOtherItem=True,
        otherText="Custom",
        visibleIf="{specifyItems}",
        **defaultOptions,
    ),
    customFunctions=vls.getJS("libtool/libtool.js"),
    customCode="""applyThemeBasedOnClass(survey);
    const observer = new MutationObserver(() => {
        applyThemeBasedOnClass(survey);
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    
    survey.onCurrentPageChanging.add((sender, options) => {
    window.abbreviation = survey.data.abbreviation
        .replaceAll(RegExp("-(?=\\\\d)", "gm"), "")
        .replaceAll("-", "_")
        .toLowerCase();
    window.pythonCode = generateDocstring(survey);
    window.quartoCode = generateDocs(survey);
    survey.getQuestionByName("output").html = `<div><p><b>
Before you download anything, please eyeball the files to check if everything was saved correctly.
See the folded sections below the buttons.
If not, go back to the previous page and correct the mistakes.
Especially check the reliability coefficients.
</b></p></div>

<div>
<p>
Below you will find the whole content of your code file. Fork the <a href='https://github.com/jakub-jedrusiak/VelesLibrary' target='_blank' rel='noopener noreferrer'>VelesLibrary repo</a>,
create the file at the appropriate location,${survey.data.specifyItems ? "" : " <b>add the necessary elements</b>,"} and commit it. Manually add anything not ordinary.
Your file should be added under <code>veleslibrary/questionnaires${survey.data.language === "en" ? "" : ("/" + survey.data.language)}/</code>.
If there's no such folder, create it and copy the default <code>__init__.py</code> file and remove the existing imports.
If you can, please also add the following instruction to the appropriate <code>__init__.py</code> file: <code>from .${window.abbreviation} import ${window.abbreviation}</code>.
</p>

<input id="downloadBtn" onclick="downloadPython()" class="sd-btn sd-btn--action sd-navigation__complete-btn" type="button" value="Download code as .py file">

<details style="margin-top: 1em;">
<summary>See the file</summary>
<pre id="pythonCode">${window.pythonCode.replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</pre>
</details>

</div>

<div>
<p>
You also need to document the questionnaire on the VelesDocs website. Fork the <a href='https://github.com/jakub-jedrusiak/VelesDocs' target='_blank' rel='noopener noreferrer'>VelesDocs repo</a>,
download the documentation file using the button below, and add it under <code>library/${survey.data.language}</code>.
If your language folder doesn't exist, create it, make a copy of the <code>en.qmd</code> file, change the language in the title,
and the language code in the contents. Commit the changes. If you made any changes to the docstring in the .py file, add them to the .qmd file.
</p>

<input id="downloadBtn" onclick="downloadQuarto()" class="sd-btn sd-btn--action sd-navigation__complete-btn" type="button" value="Download docs as .qmd file">

<details style="margin-top: 1em;">
<summary>See the file</summary>
<pre id="quartoCode">${window.quartoCode.replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</pre>
</details>

</div>

`;
});""",
)


result = vls.page(
    "output",
    vls.info("output", "Loading…"),
    customCode="survey.showCompleteButton = false;",
)

survey = vls.survey(
    form,
    result,
    path="libtool",
    pageNextText="Generate",
    themeFile="libtool/survey_theme.json",
    build=False,
)

survey.build("libtool", pauseBuild=True)
copyfile("libtool/survey_theme_dark.json", "libtool/survey/src/themeDark.json")
survey.build("libtool")

copyfile("libtool/survey/build/main.js", "libtool/main.js")
if exists("_site/libtool/main.js"):
    copyfile("libtool/survey/build/main.js", "_site/libtool/main.js")
