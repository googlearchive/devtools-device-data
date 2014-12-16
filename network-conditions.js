/** @type {!Array.<!WebInspector.OverridesSupport.NetworkConditionsPreset>} */
WebInspector.OverridesUI._networkConditionsPresets = [
    {id: "offline", title: "Offline", throughput: 0, latency: 0},
    {id: "gprs", title: "GPRS", throughput: 50, latency: 500},
    {id: "edge", title: "EDGE", throughput: 250, latency: 300},
    {id: "3g", title: "3G", throughput: 750, latency: 100},
    {id: "dsl", title: "DSL", throughput: 2 * 1024, latency: 5},
    {id: "wifi", title: "WiFi", throughput: 30 * 1024, latency: 2},
    {id: "online", title: "No throttling", throughput: WebInspector.OverridesSupport.NetworkThroughputUnlimitedValue, latency: 0}
];
