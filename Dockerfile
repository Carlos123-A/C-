FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /app

RUN dotnet new blazor -o BlazorApp

WORKDIR /app/BlazorApp

COPY TodoItem.cs /app/BlazorApp/TodoItem.cs

COPY NavMenu.razor /app/BlazorApp/Components/Layout/NavMenu.razor

COPY Todo.razor /app/BlazorApp/Components/Pages/Todo.razor

COPY Counter.razor /app/BlazorApp/Components/Pages/Counter.razor

COPY Home.razor /app/BlazorApp/Components/Pages/Home.razor

RUN dotnet restore

RUN dotnet build --configuration Release

RUN dotnet publish --configuration Release --output /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0

WORKDIR /app

COPY --from=build /app/publish .

EXPOSE 80

ENTRYPOINT ["dotnet", "BlazorApp.dll"]
