from ert.cwrap import BaseCClass, CWrapper
from ert.ecl import EclGrid
from ert.well import ECL_WELL_LIB, WellTimeLine


class WellInfo(BaseCClass):

    def __init__(self, grid, rst_file):
        """
        @type grid: EclGrid
        """
        c_ptr = WellInfo.cNamespace().alloc(grid)
        super(WellInfo, self).__init__(c_ptr)

        WellInfo.cNamespace().load_rstfile(self, rst_file)


    def __len__(self):
        """ @rtype: int """
        return WellInfo.cNamespace().get_well_count(self)


    def __getitem__(self, item):
        """
         @type item: int or str
         @rtype: WellTimeLine
        """

        if isinstance(item, str):
            if not item in self:
                raise KeyError("The well '%s' is not in this set." % item)
            well_name = item

        elif isinstance(item, int):
            if not 0 <= item < len(self):
                raise IndexError("Index must be in range 0 <= %d < %d" % (item, len(self)))
            well_name = WellInfo.cNamespace().iget_well_name(self, item)

        return WellInfo.cNamespace().get_ts(self, well_name).setParent(self)

    def __iter__(self):
        index = 0

        while index < len(self):
            yield self[index]
            index += 1


    def allWellNames(self):
        """ @rtype: list of str """
        return [WellInfo.cNamespace().iget_well_name(self, index) for index in range(0, len(self))]


    def __contains__(self, item):
        """
         @type item: str
         @rtype: bool
        """
        return WellInfo.cNamespace().has_well(self, item)


    def free(self):
        WellInfo.cNamespace().free(self)


CWrapper.registerObjectType("well_info", WellInfo)

cwrapper = CWrapper(ECL_WELL_LIB)

WellInfo.cNamespace().alloc = cwrapper.prototype("c_void_p well_info_alloc(ecl_grid)")
WellInfo.cNamespace().free  = cwrapper.prototype("void well_info_free(well_info)")

WellInfo.cNamespace().load_rstfile = cwrapper.prototype("void well_info_load_rstfile(well_info, char*)")

WellInfo.cNamespace().get_well_count = cwrapper.prototype("int well_info_get_num_wells(well_info)")
WellInfo.cNamespace().iget_well_name = cwrapper.prototype("char* well_info_iget_well_name(well_info, int)")
WellInfo.cNamespace().get_ts = cwrapper.prototype("well_time_line_ref well_info_get_ts(well_info, char*)")

WellInfo.cNamespace().has_well = cwrapper.prototype("bool well_info_has_well(well_info, char*)")

