help_text_allocation_round = """
To apply for an allocation on a system, the system must have an open allocation round. Please choose the applicable application
round for the resources you require. If the system isn't available it means applications are closed for that system."""

help_text_project_title = "Please make it informative, it may be published (100 characters max)"

help_text_project_summary = "Please make this suitable for a general audience, and highlight the aims, novelty, and significance of the outcomes.  Again, assume that the project summary will be published. (1000 characters max)."

help_text_priority_areas = """
There are currently two priority areas that each gain independent access to 25% of the Pawsey-funded infrastructure;
radio astronomy and the geosciences.<br/>
Note that your application will also be considered under the other allocation schemes."""

help_text_available_priority_areas = """
Only priority areas available for the chosen allocation round are presented here."""

help_text_research_record = """Relevant significant contributions to the research field.<br/>
Include supercomputing experience.<br/>
Include project/team management experience.<br/>
(5000 characters max).
"""

help_text_research_significance = "Include relevance to national or state priority areas (5000 characters max)."

help_text_computational_methodology = """Indicate why you need access to the supercomputer.<br/>
Describe the scaling performance of algorithms and/or software if known,
giving supporting references/examples where possible. If the code is
optimised to work on a specific architecture/interconnect provide details
of these optimisations.<br/>
Describe your workflow.   E.g. expected job size and number of simultaneous
jobs, and associated analysis/production of large data sets.<br/>
Describe codes used in your research, identifying size of jobs
in terms of number of processes, data volumes worked with, computing resources utilised etc.<br/>
(5000 characters max).
"""

help_text_core_hours="""How much compute time do you require in this allocation period?  For CPU based resources, a Service Unit is a core hour.  For GPU based resources, this is a GPU hour."""


help_text_storage_temporary="""Temporary scratch is only required during the running of jobs, including the pre/post processing of datasets (in terabytes)."""

help_text_storage_resident="""Resident storage refers to the data needed for day-to-day working, e.g. holding a number of restart files or input datasets (in terabytes)."""

help_text_storage_pbstore="""The iVEC Petascale Data Store is intended for longer term archiving of data sets, not for the above storage types (in terabytes)."""

help_text_data_transfers="""Please outline what data (if any) will be transferred from remote systems to the iVEC systems. Please describe the size and geographical location of the remote data and the expected frequency of transfers. (512 chars max.)"""

help_text_research_classifications = """<h4>Research Classifications</h4><br/>&bull; List between one and three 6-digit Field of Research codes for the project, and their weightings totalling 100%.<br/>
&bull; Codes are available from the <a href="http://www.abs.gov.au/ausstats/abs@.nsf/0/6BB427AB9696C225CA2574180004463E?opendocument" target="blank">ABS website</a>."""

help_text_project_participants = """<h4>Project Participants</h4><br/>
&bull; Enter the details of people actively participating in the project.<br/>
&bull; <b>List the person responsible for the project (Project Leader) first</b>. This person must be a non-student staff member
at an Australian university or CSIRO and obtain an iVEC login account (which will be done once the application is
approved) and will be responsible for approving additional users to the project, ensuring that appropriate progress
reports are submitted and be the primary conduit between the project team members and iVEC.<br/>
&bull; Put the proportion of their own time allocated to the project for each participant in the EFT % column.<br/>
&bull; Tick the admin box if the participant is authorised to add/delete users to/from the project, or grant access to project data.<br/>
"""

help_text_publications = """<h4>Ten Best Publications</h4><br/>
&bull; You may include refereed journal articles, conference papers, honours/postgraduate theses,
book chapters, patents, or reports.<br/>
&bull; Please include a one sentence statement for each explaining why that publication is significant.
"""

help_text_research_funding = """<h4>Research Funding Over The Last Five Years</h4><br/>
&bull; Do not include funding that supports this project as that will go in section named Supporting Funding.
"""

help_text_supporting_funding = """<h4>Supporting Funding</h4><br/>
&bull; List funding that is supporting this project.
"""

help_text_supercomputer_job = """<h4>Resource Request</h4><br/>
&bull; The data given here should be consistent with Computational Methodology.<br/>
&bull; Please specify storage in terabytes (TB).<br/>
&bull; Please fill out data for three cases - smallest, typical and largest job.
"""

help_text_libraries = """<h4>Applications, Tools or Libraries</h4><br/>
&bull; Please make sure you have access to the source code, or that a compiled version appropriate to the <i>epic</i> supercomputer is available.<br/>
&bull; Indicate in the Licensing column whether a Licence is required, and if so whether you have such a licence.<br/>
&bull; Include requirements for libraries such as SCALAPACK, FFTW and indicate if you use a common version or install your own.<br/>
&bull; If you build your own applications, libraries and/or tools please indicate which compilers you use.<br/>
&bull; For all software please include version numbers.<br/>
"""
help_text_system_name = """The common name of a shared resource."""
help_text_system_description = """Optional description field for this system."""

help_text_allocationround_system = """This round will allocate resources on this system."""
help_text_allocationround_start_date = """Applications are open as of this date..."""
help_text_allocationround_end_date = """...and closed as of this date"""
help_text_allocationround_name = """An optional label for the round to differentiate it in listings.
If left blank, the system name will be used instead."""
help_text_allocationround_priority_area = """Applications for this round can only be made for these priority areas."""


help_text_emailtemplate_name = """The name of your email template"""
help_text_emailtemplate_subject = """The subject header for emails sent using this template"""
help_text_emailtemplate_template = """Your email template body in Mako templating syntax"""
