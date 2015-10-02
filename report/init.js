function getStockSymbol() {
    var url = purl(location.search); 
    return url.param('stock_symbol') || '1101';
}

function initTitle() {
    var titleElement = document.createElement('h1');
    titleElement.innerHTML = '財務比率分析 - ' + getStockSymbol();
    var rootElement = document.getElementById('root');
    rootElement.appendChild(titleElement);
}

function initSections() {
    var rootElement = document.getElementById('root');
    rootElement.appendChild(makeSections());
}

function initCharts() {
    var stockSymbol = getStockSymbol();
    makeCapitalStructureChart(stockSymbol, 'yearly');
    makeCapitalStructureChart(stockSymbol, 'quarterly');
    makeCapitalIncreaseHistoryChart(stockSymbol);
    makeCashFlowChart(stockSymbol, 'yearly');
    makeCashFlowChart(stockSymbol, 'quarterly');
    makeCccChart(stockSymbol, 'yearly');
    makeCccChart(stockSymbol, 'quarterly');
    makeDividendPolicy(stockSymbol);
    makeDupontChart(stockSymbol, 'yearly');
    makeDupontChart(stockSymbol, 'quarterly');
    makeLiquidityChart(stockSymbol, 'yearly');
    makeLiquidityChart(stockSymbol, 'quarterly');
    makeLongTermInvestmentsToAssetsRatioChart(stockSymbol, 'yearly');
    makeLongTermInvestmentsToAssetsRatioChart(stockSymbol, 'quarterly');
    makeNetIncomeToOperatingActivitiesChart(stockSymbol, 'yearly');
    makeNetIncomeToOperatingActivitiesChart(stockSymbol, 'quarterly');
    makeOperatingRevenueChart(stockSymbol);
    makeProfitabilityChart(stockSymbol, 'yearly');
    makeProfitabilityChart(stockSymbol, 'quarterly');
    makeRevenueIndex(stockSymbol, 'yearly');
    makeRevenueIndex(stockSymbol, 'quarterly');
}

function init() {
    initTitle();
    initSections();
    initCharts(); 
}