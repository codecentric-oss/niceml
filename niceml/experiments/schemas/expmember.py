"""Module for a base ExpMember"""
from dataclasses import dataclass
from typing import List, Optional

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.expfilenames import ExperimentFilenames


@dataclass
class ExpMember:
    """ExpMember class to describe and validate experiments"""

    path: str
    member_type: str
    required: bool
    description: str

    def get_docstring(self) -> str:
        """Returns a docstring for an ExpMember"""
        doc_str = f"**File:** ``{self.path}``\n\n"
        doc_str += f":type: {self.member_type}\n"
        doc_str += f":required: {self.required}\n"
        doc_str += f":description: {self.description}\n"
        return doc_str

    def validate(self, exp_data: ExperimentData) -> bool:
        """validates the experiment given the ExperimentData"""
        return self.path in exp_data.all_exp_files

    def __lt__(self, other):
        """ExpMembers without folders come first
        otherwise sort after name"""
        own_paths = self.path.rsplit("/", maxsplit=1)
        other_paths = other.path.rsplit("/", maxsplit=1)
        if len(own_paths) < len(other_paths):
            return True
        if len(own_paths) > len(other_paths):
            return False
        return self.path < other.path


class LogCsvMember(ExpMember):
    """Specific member of the experiment containing the train logs"""

    def __init__(self):
        super().__init__(
            path=ExperimentFilenames.TRAIN_LOGS,
            required=True,
            description="This file contains all logs generated during the training",
            member_type="csv-file",
        )


class FolderMember(ExpMember):
    """This member is a folder containing arbitrary files with specific extensions"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        path: str,
        required: bool,
        description: str,
        min_required_files: int = 0,
        extensions: Optional[List[str]] = None,
    ):
        super().__init__(
            path=path, required=required, description=description, member_type="folder"
        )
        self.min_required_files = min_required_files
        self.extensions = extensions

    def get_docstring(self) -> str:
        doc_str = super().get_docstring()
        doc_str += f":min_required_files: {self.min_required_files}\n"
        if self.extensions is not None:
            ext_str = ",".join(self.extensions)
            doc_str += f":extensions: {ext_str}"
        return doc_str
