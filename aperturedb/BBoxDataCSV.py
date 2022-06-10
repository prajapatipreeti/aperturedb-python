from matplotlib.transforms import Bbox
from aperturedb import ParallelLoader
from aperturedb import CSVParser

HEADER_X_POS  = "x_pos"
HEADER_Y_POS  = "y_pos"
HEADER_WIDTH  = "width"
HEADER_HEIGHT = "height"
IMG_KEY_PROP  = "img_key_prop"
IMG_KEY_VAL   = "img_key_value"


class BBoxDataCSV(CSVParser.CSVParser):
    """
    **ApertureDB BBox Data.**

    This class loads the Bounding Box Data which is present in a csv file,
    and converts it into a series of aperturedb queries.

    .. note::
        Is backed by a csv file with the following columns:

            ``IMG_KEY``, ``x_pos``, ``y_pos``, ``width``, ``height``, ``BBOX_PROP_NAME_1``, ... ``BBOX_PROP_NAME_N``, ``constraint_BBOX_PROP_NAME_1``

    **IMG_KEY**: column has the property name of the image property that
    the bounding box will be connected to, and each row has the value
    that will be used for finding the image.

    **x_pos, y_pos**: Specify the coordinates of top left of the bounding box.

    **width, height**: Specify the dimensions of the bounding box, as integers (unit is in pixels).

    **BBOX_PROP_NAME_N**: is an arbitrary name of the property of the bounding
    box, and each row has the value for that property.

    **constraint_BBOX_PROP_NAME_1**: Constraints against specific property, used for conditionally adding a Bounding Box.

    Example csv file::

        img_unique_id,x_pos,y_pos,width,height,type,dataset_id,constraint_dataset_id
        d5b25253-9c1e,257,154,84,125,manual,12345,12345
        d5b25253-9c1e,7,537,522,282,manual,12346,12346
        ...

    Example usage:

    .. code-block:: python

        data = BBoxDataCSV("/path/to/BoundingBoxesData.csv")
        loader = ParallelLoader(db)
        loader.ingest(data)


    .. important::
        In the above example, the constraint_dataset_id ensures that a bounding box with the specified
        dataset_id would be only inserted if it does not already exist in the database.

    """

    def __init__(self, filename):

        super().__init__(filename)

        self.props_keys       = [x for x in self.header[5:]
                                 if not x.startswith(CSVParser.CONTRAINTS_PREFIX)]
        self.constraints_keys = [x for x in self.header[5:]
                                 if x.startswith(CSVParser.CONTRAINTS_PREFIX)]

        self.img_key = self.header[0]
        self.command = "AddBoundingBox"

    def getitem(self, idx):

        val = self.df.loc[idx, self.img_key]
        box_data_headers = [HEADER_X_POS,
                            HEADER_Y_POS, HEADER_WIDTH, HEADER_HEIGHT]
        box_data = [int(self.df.loc[idx, h]) for h in box_data_headers]

        q = []

        ref_counter = idx + 1
        # TODO we could reuse image references within the batch
        # instead of creating a new find for every image.
        img_ref = ref_counter
        fi = {
            "FindImage": {
                "_ref": img_ref,
            }
        }

        key = self.img_key
        val = val
        constraints = {}
        constraints[key] = ["==", val]
        fi["FindImage"]["constraints"] = constraints
        q.append(fi)

        rect_attrs = ["x", "y", "width", "height"]
        custom_fields = {
            "image": img_ref,
            "rectangle": {
                attr: val for attr, val in zip(rect_attrs, box_data)
            },
        }
        abb = self._basic_command(idx, custom_fields)

        properties  = self.parse_properties(self.df, idx)
        if properties:
            props = properties
            if "_label" in props:
                abb[self.command]["label"] = props["_label"]
                props.pop("_label")
            # Check if props is not empty after removing "_label"
            if props:
                abb[self.command]["properties"] = props
        q.append(abb)

        return q, []

    def validate(self):

        self.header = list(self.df.columns.values)

        if self.header[1] != HEADER_X_POS:
            raise Exception("Error with CSV file field: " + HEADER_X_POS)
        if self.header[2] != HEADER_Y_POS:
            raise Exception("Error with CSV file field: " + HEADER_Y_POS)
        if self.header[3] != HEADER_WIDTH:
            raise Exception("Error with CSV file field: " + HEADER_WIDTH)
        if self.header[4] != HEADER_HEIGHT:
            raise Exception("Error with CSV file field: " + HEADER_HEIGHT)
