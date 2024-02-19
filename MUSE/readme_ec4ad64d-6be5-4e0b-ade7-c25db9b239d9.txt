This file contains an overview of the structure and content of your download request from the ESO Science Archive.


For every downloaded dataset, files are listed below with the following structure:

dataset_name
        - archive_file_name (technical name, as saved on disk)	original_file_name (user name, contains relevant information) category size


Please note that, depending on your operative system and method of download, at download time the colons (:) in the archive_file_name as listed below may be replaced by underscores (_).


In order to rename the files on disk from the technical archive_file_name to the the more meaningful original_file_name, run the following shell command:
    cat THIS_FILE | awk '$2 ~ /^ADP/ {print "test -f",$2,"&& mv",$2,$3}' | sh


In case you have requested cutouts, the file name on disk contains the TARGET name that you have provided as input. To order files by it when listing them, run the following shell command:
    cat THIS_FILE | awk '$2 ~ /^ADP/ {print $2}' | sort -t_ -k3,3


Publications based on observations collected at ESO telescopes must acknowledge this fact (please see: http://archive.eso.org/cms/eso-data-access-policy.html#acknowledgement).

Your feedback regarding the data quality of the downloaded data products is greatly appreciated by contacting the ESO Archive Science Group via https://support.eso.org/ , subject: Phase 3 ... thanks!!

The downloaded processed data are characterized in detail in the following release documents:
Ref(0) VEXAS_DR1_ESO_release-description_2020.pdf https://www.eso.org/rm/api/v1/public/releaseDescriptions/146
Ref(1) IDP_MUSE_IFU_release_description_1.8.pdf https://www.eso.org/rm/api/v1/public/releaseDescriptions/78

You can download those documents with following shell command:
	 cat THIS_FILE | awk -F/ '$1 ~ /^Ref\(/ {print $0,$NF}' | awk '{printf("curl -o %s_%s %s\n", $4, $2, $3)}' | sh

ADP.2016-06-01T14:07:30.134 Ref(1)
	- ADP.2016-06-01T14:07:30.134.fits	MU_SCBC_1134385_2015-01-12T00:54:04.379_WFM-NOAO-N_OBJ.fits	SCIENCE.CUBE.IFS	2940647040
	- ADP.2016-06-01T14:07:30.135.fits	MU_SIMC_1134385_2015-01-12T00:54:04.379_WFM-NOAO-N_OBJ.fits	ANCILLARY.IMAGE.WHITELIGHT	504000
	- ADP.2016-06-01T14:07:30.136.log	r.MUSE.2015-01-12T00:54:04.379_tpl.log	ANCILLARY.README	220193
	- ADP.2016-06-01T14:07:30.137.png	r.MUSE.2015-01-12T00:54:04.379_tpl.png	ANCILLARY.PREVIEW	213100
	- ADP.2016-06-01T14:07:30.138.png	r.MUSE.2015-01-12T00:54:04.379_pst.png	ANCILLARY.PREVIEW	220357
	- ADP.2016-06-01T14:07:30.139.png	r.MUSE.2015-01-12T01:00:44.954_pst.png	ANCILLARY.PREVIEW	220488
ADP.2020-02-10T10:15:28.568 Ref(0)
	- ADP.2020-02-10T10:15:28.568.fits	VEXAS-SLICES06_A1.fits	SCIENCE.CATALOGTILE	209839680
