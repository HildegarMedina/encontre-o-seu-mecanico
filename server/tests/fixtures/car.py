from schemas.response.auth import AccessTokenResponse
from services.car import CarService
from schemas.request.car import AddCar

async def create_car(car, client, model, repo):
    car_svc = CarService(model, repo, AccessTokenResponse(**client))
    await car_svc.save(AddCar(**car))
    client = await car_svc.get_car_by_details(car["brand"], car["model"], car["version"],
                                              car["year"], client["id"])
    return dict(client)

async def destroy_car(car, client, model, repo):
    car_svc = CarService(model, repo, AccessTokenResponse(**client))
    car = await car_svc.get_car_by_details(car["brand"], car["model"], car["version"],
                                           car["year"], client["id"])
    await car_svc.delete(car["id"])
