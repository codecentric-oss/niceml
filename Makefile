install:
	poetry install -E tensorflow -E visu

install_macos:
	poetry install -E tensorflow-macos -E visu

pytest:
	poetry run pytest ./tests

generate_data:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_data_generation -c configs/jobs/job_data_generation/job_data_generation.yaml

train_semseg:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_semseg/job_train_semseg_number.yaml

train_objdet:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_objdet/job_train_objdet_number.yaml

train_regression:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_reg/job_train_reg_sinus.yaml

train_classification_multitarget:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_cls/job_train_cls_multitarget.yaml

train_classification_binary:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml

train_classification_softmax:
	poetry run dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/job_train/job_train_cls/job_train_cls_softmax.yaml

dashboard:
	poetry run streamlit run niceml/dashboard/dashboard.py configs/dashboard/local.yaml