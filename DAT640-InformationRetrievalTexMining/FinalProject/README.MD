## Final project assignment

### Team ID: Team-008
Members: 
* Asahi Cantu 
* Shaon Rahman
# Team-008	Tuesday 14:15-14:30
URL [Description](https://github.com/kbalog/ir-course/tree/master/project)

Project: [MS Marco Document re-ranking](https://microsoft.github.io/msmarco/)

# Group project

## Objectives

The objective of project work is to apply the knowledge gained in the course, in a group setting, to a selected (open) information retrieval problem.
Specifically, you'll first need to establish a reasonable baseline, then develop one or multiple advanced methods aiming to improve over the baseline. Using a standard test collection, you'll need to experimentally compare the baseline and advanced solutions.

## Weekly meeting slots

Each group is allocated a dedicated 15mins slot (during what would normally be lecture hours) to discuss their progress. It is expected that at least one member of the group is present in person.

| **Team** | **Slot** |
| -- | -- |
| Team-008 | Tuesday 14:15-14:30 |

## Deadlines

  * **Nov 6 12:00** Delivery of draft project report for feedback. The report is to be submitted in PDF format to dat640help@gmail.com with "Team-xxx draft project report" as subject. Feedback will be given during the Monday/Tuesday meeting the week after.
  * **Nov 16 16:00** Delivery of final project report. The report is to be submitted in PDF format to dat640help@gmail.com with "Team-xxx project report" as subject.

## Projects

You may choose one from the following projects:

  * **[MS Marco Document re-ranking](https://microsoft.github.io/msmarco/)**
    - Given a candidate top-100 document as retrieved by BM25, re-rank documents by relevance. This task has also run as part of the TREC 2019 Deep Learning track.
    - Document collection: MS MARCO document corpus (3.2M documents, 22GB)
    - Resources
      - [Task GitHub repo](https://github.com/microsoft/MSMARCO-Document-Ranking)
      - [Relevance judgments for evaluation topics](https://trec.nist.gov/data/cast/2019qrels.txt)
      - [TREC 2019 Deep Learning track overview](https://arxiv.org/abs/2003.07820)
 
## Workflow

  * Hand in a report using the specified project template. The page limit for the report is 4 A4 pages (in double column format).
  * Submit code and the generated output files so that we can verify your solution and results.
    * There are no restrictions on the programming language, toolkits/libraries used, etc. with the default choice being Python and the packages used in the exercises/assignments.
    * You are free to use any external data collections or resources (e.g., pre-trained embeddings) in addition to the 'official' problem datasets.
    * Some of the problems involve working with large datasets. If you need server access, you'll need to contact the Unix system administrator.
    * While you are expected to work independently as a group, you'll have the possibility to get feedback on your ideas in a regular weekly basis. For each group, there will be a weekly dedicated 15 mins slot to discuss the project with the lecturer. Also, there will be an internal intermediate deadline for getting feedback on the draft of your report.

## Timeline

While the following is merely a recommendation, it may help you to stay on course.

  * Week 1:
    - Understand the problem (and ideally complete the corresponding sections of the report)
    - Preprocess and index the document collection
    - Implement a baseline method
  * Week 2
    - Run and evaluate the baseline method
    - Implement an advanced method
    - Write up your progress so far and submit the report for feedback    
  * Week 3
    - Run and evaluate your advanced method
    - Experiment with additional methods or refinements of your advanced method
    - Finalize your report

## Report

  * Use the [ACM two-column template](https://www.acm.org/publications/proceedings-template) for the report.
  * It is highly recommended that you use LaTeX.  The ACM template is also available on [Overleaf](https://www.overleaf.com/latex/templates/acm-conference-proceedings-master-template/pnrfvrrdbfwt).

### Structure

Structure your paper according to the following sections:

  * **Introduction** - Explain the context of the problem that you are tackling, including references to relevant literature.
  * **Problem Statement** - Formalize the task (in terms of input and output) and specify important details about the data collection.
  * **Baseline Method** - Explain what you are taking as your baseline method, as well as why this is a reasonable baseline, and why you are making specific implementation choices.
  * **Advanced Method** - Explain what you are taking as your advanced method(s), as well as why this is a promising attempt to outperform the baseline method, and why you are making specific implementation choices.
  * **Results** - With tables and graphs, make a clear, concise, and digestible presentation of the data produced by your experiments. This includes describing the key facts and trend from your results.
  * **Discussion and Conclusions** - Summarize and discuss different challenges you faced and how you solved those. Include interpretations of the key facts and trends you observed and pointed out in the Results section. Which method performed best, and why? Speculate: What could you have done differently, and what consequences would that have had?


## Evaluation

Project submissions will be graded with respect the following categories:

| Category | Points |
| -- | -- |
| Problem understanding | 5 |
| Baseline method | 10 |
| Advanced method(s) | 15 |
| Report | 15 |
| Code quality | 5 |
| **Total** | **50** |

The evaluation will not be automated like in the assignments, and therefore it will primarily proceed based on qualitative categories, rather than operationalized criteria. On the one hand, this means less certainty for you regarding what level of quality is good enough for a certain grade. On the other hand, if your work is truly excellent in some aspects within a category, this can make up for more deficient aspects in the same category. In short, do your best and the evaluation will look out for opportunities to justify awarding points.

Nevertheless, keep in mind that these key aspects of each grading category are some of the ways your project submission may score points:


  * Problem understanding
    - Demonstrating your understanding of the chosen project and associated task.
	- Clearly explaining the problem at hand, and the challenges it may entail.
	- Identifying main families of approaches developed for the task at hand (a literature review).
  * Baseline method
    - Selecting a sensible baseline, implementing and evaluating it experimentally.
  * Advanced method(s)
    - Selecting an interesting or performant advanced method, implementing and evaluating it experimentally.
    - Motivating, designing and implementing one or multiple advanced approaches.
	    - Either extending the baseline,
		- Employing a completely different approach found in the literature, or
		- Designing a method of your own.
	- Clarity of argumentation
	- Creativity
	- Demonstrating understanding of the advanced methods
	- Extensiveness of the experiments
	- Overall performance (improvements over baseline).
  * Report
    - Clearly explaining the motivation or rationale behind the choices made.
	- Documenting key technical decisions to support future reproducibility.
	    - This requires details with accessible wording and structure in a way that your results are reproducible based on the provided description.
	- Producing insight into the process through analysis and discussion of results.
	- Effectively using visual tools, such as illustrations, plots and tables to support and communicate your findings.
  * Code quality
    - Clearly structured and readable code.
	- Readability includes sensible variable/method naming conventions and adding docstrings/comments where necessary.


https://www.overleaf.com/project/5f9daabc0f92c00001ecdc


https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docs-lookup.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-doctrain-queries.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-queries.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-top100.gz
https://msmarco.blob.core.windows.net/msmarcoranking/msmarco-docdev-qrels.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/docleaderboard-queries.tsv.gz
https://msmarco.blob.core.windows.net/msmarcoranking/docleaderboard-top100.tsv.gz


life against death
## Elastic Search
MS-MARCO:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDZhMGZlNDZlZWYzMzRmYWRhNzJhYmM5MTkzM2I1NGU4JGI1YzE1MWYwMmUwMTRkNTdiZWRjN2UwZThmMmU5OTNk
### ES
  https://6a0fe46eef334fada72abc91933b54e8.us-central1.gcp.cloud.es.io:9243
### Kibana
  https://b5c151f02e014d57bedc7e0e8f2e993d.us-central1.gcp.cloud.es.io:9243
cloud.elastic.co
User Name:elastic
Password: IfKREtTr7fCqMYTD8NKE4yBi
