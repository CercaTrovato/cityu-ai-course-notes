candidates = {"ridge": Ridge(alpha=100),
              "lasso": Lasso(alpha=0.001, max_iter=100000)}
for name, estimator in candidates.items():
    model = make_pipeline(StandardScaler(), estimator)
    model.fit(train[x_names], train["market_excess_return"])
    forecast[name] = model.predict(test[x_names])