# from ..model.catalog import Catalog
# from ..schema import CatalogInput, CatalogType
# from ..repository.catalog import CatalogRepository
# 
# 
# class CatalogService:
# 
#     @staticmethod
#     async def add_catalog(catalog_data: CatalogInput):
#         catalog = Catalog(
#             name=catalog_data.name,
#             description=catalog_data.description
#         )
#         catalog.name = catalog_data.name
#         catalog.description = catalog_data.description
#         await CatalogRepository.asyn_create(catalog)
# 
#         return CatalogType(
#             id=catalog.id,
#             name=catalog.name,
#             description=catalog.description
#         )
# 
#     @staticmethod
#     async def get_all_catalogs():
#         list_catalog = await CatalogRepository.get_all()
#         return [CatalogType(
#             id=catalog.id,
#             name=catalog.name,
#             description=catalog.description
#         ) for catalog in list_catalog]
# 
#     @staticmethod
#     async def get_by_id(catalog_id: int) -> CatalogType:
#         catalog = await CatalogRepository.get_by_id(catalog_id)
#         if catalog is None:
#             return CatalogType(
#                 id=0,
#                 name="",
#                 description=""
#             )
#         return CatalogType(
#             id=catalog.id,
#             name=catalog.name,
#             description=catalog.description
#         )
# 
#     @staticmethod
#     async def delete(catalog_id: int):
#         await CatalogRepository.delete(catalog_id)
#         return f"Successfully deleted catalog with id {catalog_id}"
# 
#     @staticmethod
#     async def update(catalog_id: int, catalog_data: CatalogInput):
#         catalog = Catalog(name=catalog_data.name,
#                           description=catalog_data.description) # type: ignore
#                 
#         await CatalogRepository.update(catalog_id, catalog)
#         return f"Successfully updated catalog with id {catalog_id}"
#         # End of Selection
