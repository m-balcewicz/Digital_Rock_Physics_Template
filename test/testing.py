import import_export_data as ie


def load_test_data(**kwargs):
    """
    Loads test data from a raw file.

    Args:
        **kwargs: Optional arguments for file_path and dimension.

    Returns:
        A numpy array containing the test data and the dimension of the data.
    """
    file_path = './test/test_data.raw'
    dimension = 100

    try:
        test_data = ie.import_test(file_path, dimension=dimension)
    except Exception as e:
        raise Exception(f'Error loading test data: {e}')

    return test_data
