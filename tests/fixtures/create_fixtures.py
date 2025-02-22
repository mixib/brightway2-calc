from bw_processing import create_datapackage, INDICES_DTYPE, UNCERTAINTY_DTYPE
from fs.zipfs import ZipFS
from pathlib import Path
import json
import numpy as np


fixture_dir = Path(__file__).resolve().parent


def bw2io_example_database():
    try:
        import bw2data as bd
        import bw2io as bi
        from bw2data.backends.schema import ActivityDataset as AD

        if "__fixture_creation__" in bd.projects:
            bd.projects.delete_project("__fixture_creation__", delete_dir=True)

        bd.projects.set_current("__fixture_creation__")
        bi.add_example_database()
        db = bd.Database("Mobility example")
        method = bd.Method(("IPCC", "simple"))

        db.filepath_processed().rename(fixture_dir / "bw2io_example_db.zip")
        method.filepath_processed().rename(fixture_dir / "ipcc_simple.zip")
        with open(fixture_dir / "bw2io_example_db_mapping.json", "w") as f:
            json.dump([(obj.name, obj.id) for obj in AD.select()], f)

        bd.projects.delete_project(delete_dir=True)
    except ImportError:
        print("Can't import libraries for bw2io example database fixture creation")


def empty_biosphere():
    # Flow 1: The flow
    # Activity 1: The activity

    dp = create_datapackage(
        fs=ZipFS(str(fixture_dir / "empty_biosphere.zip"), write=True),
    )

    data_array = np.array([1, 2, 3])
    indices_array = np.array([(2, 1), (1, 1), (2, 2)], dtype=INDICES_DTYPE)
    flip_array = np.array([1, 0, 0], dtype=bool)
    dp.add_persistent_vector(
        matrix="technosphere_matrix",
        data_array=data_array,
        name="eb-technosphere",
        indices_array=indices_array,
        nrows=3,
        flip_array=flip_array,
    )

    data_array = np.array([1])
    indices_array = np.array([(1, 0)], dtype=INDICES_DTYPE)
    dp.add_persistent_vector(
        matrix="characterization_matrix",
        data_array=data_array,
        name="eb-characterization",
        indices_array=indices_array,
        global_index=0,
        nrows=1,
    )

    dp.finalize_serialization()


def create_basic_fixture():
    # Activities: 1, 2
    # Products: 1, 2
    # Biosphere flows: 1
    dp = create_datapackage(fs=ZipFS(str(fixture_dir / "basic_fixture.zip"), write=True),)

    data_array = np.array([1, 1, 0.5])
    indices_array = np.array([(1, 1), (2, 2), (2, 1)], dtype=INDICES_DTYPE)
    flip_array = np.array([0, 0, 1], dtype=bool)
    dp.add_persistent_vector(
        matrix="technosphere_matrix",
        data_array=data_array,
        name="technosphere",
        indices_array=indices_array,
        flip_array=flip_array,
    )

    data_array = np.array([1])
    indices_array = np.array([(1, 1)], dtype=INDICES_DTYPE)
    dp.add_persistent_vector(
        matrix="biosphere_matrix",
        data_array=data_array,
        name="biosphere",
        indices_array=indices_array,
    )

    data_array = np.array([1])
    indices_array = np.array([(1, 0)], dtype=INDICES_DTYPE)
    dp.add_persistent_vector(
        matrix="characterization_matrix",
        data_array=data_array,
        name="eb-characterization",
        indices_array=indices_array,
        global_index=0,
        nrows=1,
    )

    dp.finalize_serialization()


def create_svdm_fixtures():
    dp = create_datapackage(fs=ZipFS(str(fixture_dir / "svdm.zip"), write=True), sequential=True)

    data_array = np.array([42])
    indices_array = np.array([(1, 1)], dtype=INDICES_DTYPE)
    distributions_array = np.array(
        [
            (4, 0.5, np.NaN, np.NaN, 0.2, 0.8, False),
        ],
        dtype=UNCERTAINTY_DTYPE
    )
    dp.add_persistent_vector(
        matrix="weighting_matrix",
        data_array=data_array,
        name="weighting",
        indices_array=indices_array,
        distributions_array=distributions_array,
    )

    data_array = np.array([1, 2, 3, 4, 5]).reshape((1, 5))
    indices_array = np.array([(1, 1)], dtype=INDICES_DTYPE)
    dp.add_persistent_array(
        matrix="weighting_matrix",
        data_array=data_array,
        name="weighting2",
        indices_array=indices_array,
    )

    dp.finalize_serialization()

    dp2 = create_datapackage(fs=ZipFS(str(fixture_dir / "svdm2.zip"), write=True))

    data_array = np.array([88])
    indices_array = np.array([(2, 2)], dtype=INDICES_DTYPE)
    dp2.add_persistent_vector(
        matrix="weighting_matrix",
        data_array=data_array,
        name="weighting3",
        indices_array=indices_array,
    )
    dp2.finalize_serialization()


def create_mc_basic():
    # Flow 1: biosphere
    # Flow 2: biosphere
    # Flow 3: activity 1
    # Flow 4: activity 2
    # Activity 1
    # Activity 2
    dp = create_datapackage(
        fs=ZipFS(str(fixture_dir / "mc_basic.zip"), write=True),
    )

    data_array = np.array([1, 1, 0.5])
    indices_array = np.array([(3, 1), (4, 2), (4, 1)], dtype=INDICES_DTYPE)
    flip_array = np.array([0, 0, 1], dtype=bool)
    distributions_array = np.array(
        [
            (0, 1, np.NaN, np.NaN, np.NaN, np.NaN, False),
            (0, 1, np.NaN, np.NaN, np.NaN, np.NaN, False),
            (4, 0.5, np.NaN, np.NaN, 0.2, 0.8, False),
        ],
        dtype=UNCERTAINTY_DTYPE
    )
    dp.add_persistent_vector(
        matrix="technosphere_matrix",
        data_array=data_array,
        name="mc-technosphere",
        indices_array=indices_array,
        distributions_array=distributions_array,
        nrows=3,
        flip_array=flip_array,
    )

    data_array = np.array([1, 0.1])
    indices_array = np.array([(1, 1), (2, 2)], dtype=INDICES_DTYPE)
    distributions_array = np.array(
        [
            (4, 1, np.NaN, np.NaN, 0.5, 1.5, False),
            (4, 0.1, np.NaN, np.NaN, 0, 0.2, False),
        ],
        dtype=UNCERTAINTY_DTYPE
    )
    dp.add_persistent_vector(
        matrix="biosphere_matrix",
        data_array=data_array,
        name="mc-biosphere",
        indices_array=indices_array,
        distributions_array=distributions_array,
    )

    data_array = np.array([1, 2])
    indices_array = np.array([(1, 0), (2, 0)], dtype=INDICES_DTYPE)
    distributions_array = np.array(
        [
            (4, 1, np.NaN, np.NaN, 0.5, 2, False),
            (4, 2, np.NaN, np.NaN, 1, 4, False),
        ],
        dtype=UNCERTAINTY_DTYPE
    )
    dp.add_persistent_vector(
        matrix="characterization_matrix",
        data_array=data_array,
        name="mc-characterization",
        indices_array=indices_array,
        distributions_array=distributions_array,
        global_index=0,
        nrows=3,
    )
    dp.finalize_serialization()


# def create_mc_single_activity_only_production():
#     with temporary_project_dir() as td:
#         biosphere = bw2data.Database("biosphere")
#         biosphere.write(
#             {("biosphere", "1"): {"type": "emission"},}
#         )
#         saop = bw2data.Database("saop")
#         saop.write(
#             {
#                 ("saop", "1"): {
#                     "exchanges": [
#                         {
#                             "amount": 0.5,
#                             "minimum": 0.2,
#                             "maximum": 0.8,
#                             "input": ("biosphere", "1"),
#                             "type": "biosphere",
#                             "uncertainty type": 4,
#                         },
#                         {
#                             "amount": 1,
#                             "minimum": 0.5,
#                             "maximum": 1.5,
#                             "input": ("saop", "1"),
#                             "type": "production",
#                             "uncertainty type": 4,
#                         },
#                     ],
#                     "type": "process",
#                 },
#             }
#         )
#         fixture_dir = this_dir / "mc_saop"
#         fixture_dir.mkdir(exist_ok=True)
#         biosphere.filepath_processed().rename(fixture_dir / "biosphere.zip")
#         saop.filepath_processed().rename(fixture_dir / "saop.zip")
#         with open(fixture_dir / "mapping.json", "w") as f:
#             json.dump(list(bw2data.mapping.items()), f)


if __name__ == "__main__":
    empty_biosphere()
    bw2io_example_database()
    create_mc_basic()
    create_basic_fixture()
    create_svdm_fixtures()

#     create_example_database()
#     create_empty_biosphere()
#     create_mc_single_activity_only_production()
