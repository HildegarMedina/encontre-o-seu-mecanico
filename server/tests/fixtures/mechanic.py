from services.mechanic import MechanicService
from schemas.request.mechanic import CreateMechanic

async def create_mechanic(mechanic, model, repo):
    mechanic_svc = MechanicService(model, repo)
    await mechanic_svc.save(CreateMechanic(**mechanic))
    mechanic = await mechanic_svc.get_mechanic_by_email(mechanic['email'])
    return dict(mechanic)

async def destroy_mechanic(mechanic, model, repo):
    mechanic_svc = MechanicService(model, repo)
    mechanic = await mechanic_svc.get_mechanic_by_email(mechanic['email'])
    await mechanic_svc.delete(mechanic["id"])
