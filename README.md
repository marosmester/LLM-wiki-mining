# LLM-wiki-mining
This repository is the final output of the team project: <em> Mining data about people from Wikipedia using LLMs </em> which took place during the summer semester of the academic year 2024/2025 at FEE CTU in Prague.

## Content
This repository can be divided into 4 distinct parts. <br>
1) <strong> The annotation tool. </strong> <br>
The annotation tool is a GUI interface written in Python meant to be used by human annotators with the goal of creating ground truth annotations of people from Wikipedia. The installation manual and annotation instrucitons can be found in the [corresponding folder](annotation_tool).

2) <strong> Baseline annotation using regular expressions. </strong> <br>
This runnable [Python script](regex_annotation) which creates similar annotations as the annotation tool, but only using regular expressions. It can only provide year of birth and the year (or year span) written in image captions.

3) <strong> Annotation using LLMs. </strong> <br>
This runnable [Python script](LLM_annotation) utilizes open source large language models to provide the same annoation as humans would. The type of the LLM and the specific prompt can be selected.

4) <strong> [Statistical analysis and visualization.]() </strong> <br>
Jupyter notebook capable of visualizing the annotation's accuracy, coverage and other metrics. Avalaible in the corresponding folder.