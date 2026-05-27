class aeroporto(areroprto_Model)
    id = int
    created_at : optionale = None

    class config :
        from_attributes = true
class paginateResponse(BaseModel);
    page : int
    size : int
    total : int