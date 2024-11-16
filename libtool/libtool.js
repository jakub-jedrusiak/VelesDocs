function generateDocstring(survey) {
  const cleanAbbreviation = survey.data.abbreviation
    .replaceAll(RegExp("-(?=\\d)", "gm"), "")
    .replaceAll("-", "_");

  const adaptationString = survey.data.isAdaptation
    ? `    ## Adaptation:
${survey.data.adaptation.replaceAll(RegExp("^ *", "gm"), "        ")}

`
    : "";

  const subscalesString = survey.data.hasSubscales
    ? survey.data.subscales
        .map(
          (item, index) => `        ${index + 1}. ${item.name}: ${item.items}`
        )
        .join("\\n")
    : "        None.";

  const subscalesReliabilityString = survey.data.hasSubscales
    ? `
${
  survey.data.reliability ? "\\n        ### Subscales\\n" : ""
}${survey.data.subscales
        .map(
          (item, index) =>
            `        ${survey.data.reliability ? "    " : ""}${index + 1}. ${
              item.name
            }: α = ${item.reliability
              .toString()
              .replace(RegExp("^0", "gm"), "")}`
        )
        .join("\\n")}
`
    : "\\n";

  const text = `"""${survey.data.name} (${survey.data.abbreviation})"""
import velesresearch as vls
from velesresearch.models import PageModel

def ${cleanAbbreviation.toLowerCase()}(
    name: str = "${cleanAbbreviation}",
    instruction: str | None = None,
    questionOptions: dict | None = None,
    pageOptions: dict | None = None,
) -> PageModel:
    """
    ## ${survey.data.name} (${survey.data.abbreviation})
        ${survey.data.description}
    
    ## Original
${survey.data.original.replaceAll(RegExp("^ *", "gm"), "        ")}
    
${adaptationString}    ## ## Score calculation
        ${survey.data.scoring.replace(RegExp("([^\\.\\n])$", "gm"), "$1.")}

    ## Reverse items
        ${survey.data.hasReverseItems ? survey.data.reverse_items : "None."}
    
    ## Subscales
${subscalesString}

    ## Reliability${
      survey.data.reliability
        ? `\\n        α = ${survey.data.reliability
            .toString()
            .replace(RegExp("^0", "gm"), "")}`
        : ""
    }${subscalesReliabilityString}
    ## Implemented by
${survey.data.authors
  .map(
    (author) =>
      `        ${author.name} ${author.surname} (${author.affiliation})`
  )
  .join("\\n")}

    Args:
        name (str): Base name for pages and questions. Defaults to "${cleanAbbreviation}".
        instruction (str): Instruction for the questionnaire. None means that the default instruction will be used.
        questionOptions (dict | None): Additional options for questions as a dictionary. Defaults to None.
        pageOptions (dict | None): Additional options for pages as a dictionary. Defaults to None.

    Returns:
        PageModel: PageModel with the ${
          survey.data.abbreviation
        } questionnaire. Use the \`*\` operator to unpack it to questions.
    """
    if instruction is None:
        instruction = "" # TODO: Put your instruction here

    if questionOptions is None:
        questionOptions = {}

    if pageOptions is None:
        pageOptions = {}

    items = """""".split( # TODO: Put your items in the quotes
        "\\\\n" # TODO: Adapt the split() argument to your items
    )

    scale = """""".split( # TODO: Put your scale in the quotes
        "\\\\n" # TODO: Adapt the split() argument to your scale
    )

    return vls.page(
        name + "_page",
        vls.info(name + "_instruction", instruction),
        vls.radio(
            name,
            items,
            scale,
            **questionOptions,
        ),
        **pageOptions,
    )
`;

  return text;
}

import * as themeDark from "./themeDark.json";

function applyThemeBasedOnClass(survey) {
  const body = document.body;
  if (body.classList.contains("quarto-dark")) {
    survey.applyTheme(themeDark);
  } else if (body.classList.contains("quarto-light")) {
    survey.applyTheme(theme);
  }
}
