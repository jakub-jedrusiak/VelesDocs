from shutil import copyfile
from os.path import exists
import velesresearch as vls
from veleslibrary.questionnaires.tls15 import tls15

defaultOptions = {"isRequired": True, "autocomplete": "off"}

commaValidator = vls.regexValidator(
    r"^(\d+, )*\d+$",
    'Use comma separated values, e.g. "1, 3, 5". Put spaces between commas.',
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
            min=0,
            max=1,
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
        min=0,
        max=1,
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
    survey.getQuestionByName("output").html = `<p>Below you will find the whole content of your file. Fork the <a href='https://github.com/jakub-jedrusiak/VelesLibrary' target='_blank' rel='noopener noreferrer'>VelesLibrary repo</a>,
create the file, <b>add the necessary elements</b> and commit it. Manually add anything not ordinary. Your file should be added under veleslibrary/questionnaires${survey.data.language === "en" ? "" : ("/" + survey.data.language)}/
If there's no such folder, create it and copy the default <code>__init__.py</code> file and remove the existing imports.
If you can, please also add the following instruction to the appropriate <code>__init__.py</code> file: <code>from .${window.abbreviation} import ${window.abbreviation}</code>.</p>
<input id="downloadBtn" onclick="downloadPython()" class="sd-btn sd-btn--action sd-navigation__complete-btn" type="button" value="Download as .py file">
<details style="margin-top: 1em;">
<summary>See the file</summary>
<pre id="pythonCode">${window.pythonCode.replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</pre>
</details>`;
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
