import pandas as pd

ml = {
    "Support Vector Machines": svm.SVC(),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "SGDClassifier": linear_model.SGDClassifier(),
    "NearestCentroid": neighbors.NearestCentroid()
}

results = []
for x in ml:
    model = ml[x]
    model.fit(X_train, y_train)
    model.predict(X_test)
    accuracy = model.score(X_test, Y_test)
    results.append({
        "name": x,
        "Accuracy": accuracy
    })

pd.DataFrame(results).sort_values("Accuracy", ascending=False)