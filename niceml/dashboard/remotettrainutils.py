"""module for the loading the experiments for the dashboard"""
from typing import List, Optional

from nicegui import ui

from niceml.data.dataloaders.factories.dfloaderfactory import DfLoaderFactory
from niceml.data.dataloaders.factories.imageloaderfactory import ImageLoaderFactory
from niceml.data.dataloaders.interfaces.dfloader import DfLoader
from niceml.data.dataloaders.interfaces.imageloader import ImageLoader
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.expdatastorageloader import create_expdata_from_storage
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentdownloader import ExperimentDownloader
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.experimentmanager import ExperimentManager
from niceml.experiments.localexperimentcache import ExperimentCache


def exp_manager_factory(*params):
    """Factory for the experiment manager cached with streamlit"""
    return ExperimentManager([])


def query_experiments(storage: StorageInterface) -> List[ExperimentInfo]:
    """Query the experiments from the cloud storage"""

    def _local_query_exps(*args):
        exp_info_list: List[ExperimentInfo] = storage.list_experiments()
        return exp_info_list

    return _local_query_exps(id(storage))


def select_to_load_exps(
    exp_info_list: List[ExperimentInfo], exp_manager: ExperimentManager
):
    """Select the experiments to load.
    That means which are not in the experiment manager"""
    experiments_to_load = []
    for exp_info in exp_info_list:
        if exp_info not in exp_manager:
            experiments_to_load.append(exp_info)
    return experiments_to_load


def try_remote_exp_data_factory(
    filepath, storage, df_loader, image_loader
) -> Optional[ExperimentData]:
    """Try to load experiment data from the filepath with the remote cloud storage"""
    try:
        return create_expdata_from_storage(
            filepath, storage, df_loader=df_loader, image_loader=image_loader
        )
    except FileNotFoundError:
        return None


# pylint: disable=too-many-locals
def load_experiments(
    storage,
    exp_info_list: List[ExperimentInfo],
    df_loader_factory: DfLoaderFactory,
    image_loader_factory: ImageLoaderFactory,
    local_exp_cache: Optional[ExperimentCache] = None,
):
    """Load the experiments from the cloud storage and
    stores them in the experiment manager. Additionally, they are saved in the local cache"""
    experiments: List[ExperimentData]
    dir_info_list: List[str] = []
    load_exp_info_list: List[ExperimentInfo] = []

    # pylint: disable = unused-argument
    def _check_and_load_cache(
        *args,
    ) -> List[ExperimentData]:
        experiments_list = []
        for cur_exp_info in exp_info_list:
            if local_exp_cache is not None and cur_exp_info.short_id in local_exp_cache:
                initialized_df_loader: DfLoader = df_loader_factory.create_df_loader(
                    storage, cur_exp_info.exp_filepath
                )
                initialized_image_loader: ImageLoader = (
                    image_loader_factory.create_image_loader(
                        storage, cur_exp_info.exp_filepath
                    )
                )
                exp_data = local_exp_cache.load_experiment(
                    cur_exp_info.short_id,
                    df_loader=initialized_df_loader,
                    image_loader=initialized_image_loader,
                )
                experiments_list.append(exp_data)
            else:
                dir_info_list.append(cur_exp_info.exp_filepath)
                load_exp_info_list.append(cur_exp_info)
        return experiments_list

    exp_cache_count = local_exp_cache.get_exp_count_in_cache()
    experiments = _check_and_load_cache(exp_info_list, exp_cache_count)
    if len(load_exp_info_list) > 0:
        load_exp_count = len(load_exp_info_list)
        # prog_bar = st.progress(0)
        # status_text = st.empty()
        # status_text.text(f"Cached 0/{load_exp_count} experiments")

        for idx, dir_info in enumerate(dir_info_list):
            df_loader = df_loader_factory.create_df_loader(storage, dir_info)
            image_loader = image_loader_factory.create_image_loader(storage, dir_info)
            experiment = try_remote_exp_data_factory(
                dir_info, storage, df_loader=df_loader, image_loader=image_loader
            )
            if experiment is not None:
                experiments.append(experiment)
                if (
                    local_exp_cache is not None
                    and experiment.get_short_id() not in local_exp_cache
                ):
                    local_exp_cache.save_experiment(experiment)
            # prog_bar.progress(idx / load_exp_count)
            # status_text.text(f"Cached {idx}/{load_exp_count} experiments")
        # status_text.text(f"Cached {load_exp_count}/{load_exp_count} experiments")
        # prog_bar.progress(1.0)
        # st.success("Done")
    return experiments


def download_visu(experiment_downloader: ExperimentDownloader):
    """Download the visualization files for the experiment"""

    def download(*args):
        container.clear()
        selected_extensions = []
        for checkbox in checkboxes:
            if checkbox.value:
                selected_extensions.append(checkbox.text)

        to_download_files = experiment_downloader.get_downloads(selected_extensions)
        download_count = len(to_download_files)
        with container:
            status_bar = ui.linear_progress(0)
            status_text = ui.label()
            for idx, download_file in enumerate(to_download_files):
                status_text.text = (
                    f"({idx+1}/{download_count}) - File: {download_file.source_file}"
                )
                status_bar.set_value((idx + 1) / download_count)
                download_file()

    checkboxes = []
    for ext in experiment_downloader.get_all_extensions():
        checkboxes.append(ui.checkbox(ext))
    ui.button("Download", on_click=lambda: download())
    container = ui.column().classes("w-full")
