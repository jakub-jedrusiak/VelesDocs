function generateDocstring(survey) {
  const cleanAbbreviation = survey.data.abbreviation
    .replaceAll("-", "_")
    .replaceAll(RegExp("_(?=\\d)", "gm"), "");

  const adaptationString = survey.data.isAdaptation
    ? `    ## Adaptation:
${survey.data.adaptation.replaceAll(RegExp("^ *", "gm"), "        ")}

`
    : "";

  const subscalesString = survey.data.hasSubscales
    ? survey.data.subscales
        .map(
          (item, index) =>
            `        ${index + 1}. ${item.name}: ${item.items.replaceAll(
              RegExp(",(?! )", "gm"),
              ", "
            )}`
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

  const interactiveItems = survey.data.specifyItems;

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
${survey.data.original
  .replaceAll(RegExp("^ *", "gm"), "        ")
  .replaceAll(RegExp("(https?://.+?)(?=\\<)", "gm"), "<$1>")}
    
${adaptationString}    ## Score calculation
        ${survey.data.scoring.replace(RegExp("([^\\.\\n])$", "gm"), "$1.")}

    ## Reverse items
        ${
          survey.data.hasReverseItems
            ? survey.data.reverse_items.replaceAll(RegExp(",(?! )", "gm"), ", ")
            : "None."
        }
    
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
        instruction = """${survey.data.instruction || ""}"""${
    interactiveItems ? "" : " # TODO: Put your instruction here"
  }

    if questionOptions is None:
        questionOptions = {}

    if pageOptions is None:
        pageOptions = {}

    items = """${survey.data.items || ""}""".split(${
    interactiveItems ? "" : " # TODO: Put your items in the quotes"
  }
        ${interactiveItems ? `"${survey.data.items_separator}"` : '"\\n"'}${
    interactiveItems ? "" : " # TODO: Adapt the split() argument to your items"
  }
    )

    scale = """${survey.data.scale || ""}""".split(${
    interactiveItems ? "" : " # TODO: Put your scale in the quotes"
  }
  ${interactiveItems ? `"${survey.data.scale_separator}"` : '"\\n"'}${
    interactiveItems ? "" : " # TODO: Adapt the split() argument to your scale"
  }
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

function generateDocs(survey) {
  const cleanAbbreviation = survey.data.abbreviation
    .replaceAll("-", "_")
    .replaceAll(RegExp("_(?=\\d)", "gm"), "")
    .toLowerCase();

  const adaptationString = survey.data.isAdaptation
    ? `## Adaptation:
${survey.data.adaptation.replaceAll(RegExp("^ *", "gm"), "")}

`
    : "";

  const subscalesString = survey.data.hasSubscales
    ? survey.data.subscales
        .map(
          (item, index) =>
            `${index + 1}. ${item.name}: ${item.items.replaceAll(
              RegExp(",(?! )", "gm"),
              ", "
            )}`
        )
        .join("\\n")
    : "        None.";

  const subscalesReliabilityString = survey.data.hasSubscales
    ? `
${survey.data.reliability ? "\\n### Subscales\\n" : ""}${survey.data.subscales
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

  const text = `"""---
title: "${survey.data.name} (${survey.data.abbreviation})"
subtitle: "\`${cleanAbbreviation}()\`"
description: "${survey.data.description}"
categories: ${JSON.stringify(
    survey.data.grand_categories
      .concat(survey.data.subcategories.map((item) => item.text))
      .filter((item) => item !== undefined)
  )}
---

## Module
\`velesresearch.questionnaires.${
    survey.data.language === "en" ? "" : survey.data.language + "."
  }${cleanAbbreviation}\`

## Import
\`\`\` python
from velesresearch.questionnaires.${
    survey.data.language === "en" ? "" : survey.data.language + "."
  }${cleanAbbreviation} import ${cleanAbbreviation}
\`\`\`

## Original
${survey.data.original
  .replaceAll(RegExp("^ *", "gm"), "")
  .replaceAll(RegExp("(https?://.+?)(?=\\<)", "gm"), "<$1>")}
    
${adaptationString}## Score calculation
        ${survey.data.scoring.replace(RegExp("([^\\.\\n])$", "gm"), "$1.")}

## Reverse items
    ${
      survey.data.hasReverseItems
        ? survey.data.reverse_items.replaceAll(RegExp(",(?! )", "gm"), ", ")
        : "None."
    }
    
## Subscales
${subscalesString}

## Reliability${
    survey.data.reliability
      ? `\\nα = ${survey.data.reliability
          .toString()
          .replace(RegExp("^0", "gm"), "")}`
      : ""
  }${subscalesReliabilityString}
## Implemented by
${survey.data.authors
  .map((author) => `${author.name} ${author.surname} (${author.affiliation})`)
  .join("\\n")}

## Args
\`name\` : *str*<br>
Base name for pages and questions. Defaults to "${cleanAbbreviation}".

\`instruction\` : *str*<br>
Instruction for the questionnaire. None means that the default instruction will be used.

\`questionOptions\` : *dict | None*<br>
Additional options for questions as a dictionary. Defaults to None.

\`pageOptions\` : *dict | None*<br>
Additional options for pages as a dictionary. Defaults to None.


## Returns
\`PageModel\`<br>
PageModel with the ${
    survey.data.abbreviation
  } questionnaire. Use the \`*\` operator to unpack it to questions.
`;

  return text.replaceAll(RegExp("^ +", "gm"), "");
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
