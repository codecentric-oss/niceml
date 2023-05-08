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

dashboard:
	poetry run streamlit run niceml/dashboard/dashboard.py configs/dashboard/local.yaml

patch_mac_m1:
	conda install -y grpcio --force-reinstall