'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, TrendingUp, TrendingDown, RefreshCw } from 'lucide-react';

interface BacktestResult {
    winRate: number;
    totalReturn: number;
    trades: number;
    maxDrawdown: number;
}

export default function BacktestWidget() {
    const [isRunning, setIsRunning] = useState(false);
    const [result, setResult] = useState<BacktestResult | null>(null);
    const [params, setParams] = useState({
        entryRsi: 30,
        exitRsi: 70,
        stopLoss: 5,
        takeProfit: 10,
    });

    const runBacktest = async () => {
        setIsRunning(true);
        setResult(null);

        // Simulate backtest calculation
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Generate mock results based on parameters
        const baseWinRate = 55 + (params.entryRsi < 35 ? 5 : 0) + (params.takeProfit > params.stopLoss * 1.5 ? 5 : -5);
        const winRate = Math.min(75, Math.max(40, baseWinRate + (Math.random() * 10 - 5)));
        const trades = Math.floor(100 + (100 - params.entryRsi) * 2);
        const totalReturn = ((winRate / 100) * params.takeProfit - ((100 - winRate) / 100) * params.stopLoss) * trades / 10;

        setResult({
            winRate: Math.round(winRate * 10) / 10,
            totalReturn: Math.round(totalReturn * 10) / 10,
            trades,
            maxDrawdown: Math.round((Math.random() * 15 + 5) * 10) / 10,
        });

        setIsRunning(false);
    };

    return (
        <motion.div
            className="glass-card p-6 max-w-md mx-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
        >
            <div className="flex items-center gap-2 mb-6">
                <TrendingUp className="w-5 h-5 text-accent" />
                <h3 className="text-lg font-bold">Strategy Backtest</h3>
                <span className="text-xs font-mono text-foreground-muted ml-auto">DEMO</span>
            </div>

            {/* Parameters */}
            <div className="space-y-4 mb-6">
                <div>
                    <label className="text-xs font-mono text-foreground-muted block mb-2">
                        RSI Entry Level: {params.entryRsi}
                    </label>
                    <input
                        type="range"
                        min="10"
                        max="50"
                        value={params.entryRsi}
                        onChange={(e) => setParams({ ...params, entryRsi: Number(e.target.value) })}
                        className="w-full accent-accent"
                    />
                </div>

                <div>
                    <label className="text-xs font-mono text-foreground-muted block mb-2">
                        RSI Exit Level: {params.exitRsi}
                    </label>
                    <input
                        type="range"
                        min="50"
                        max="90"
                        value={params.exitRsi}
                        onChange={(e) => setParams({ ...params, exitRsi: Number(e.target.value) })}
                        className="w-full accent-accent"
                    />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="text-xs font-mono text-foreground-muted block mb-2">
                            Stop Loss: {params.stopLoss}%
                        </label>
                        <input
                            type="range"
                            min="1"
                            max="15"
                            value={params.stopLoss}
                            onChange={(e) => setParams({ ...params, stopLoss: Number(e.target.value) })}
                            className="w-full accent-accent"
                        />
                    </div>
                    <div>
                        <label className="text-xs font-mono text-foreground-muted block mb-2">
                            Take Profit: {params.takeProfit}%
                        </label>
                        <input
                            type="range"
                            min="2"
                            max="30"
                            value={params.takeProfit}
                            onChange={(e) => setParams({ ...params, takeProfit: Number(e.target.value) })}
                            className="w-full accent-accent"
                        />
                    </div>
                </div>
            </div>

            {/* Run Button */}
            <motion.button
                onClick={runBacktest}
                disabled={isRunning}
                className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                {isRunning ? (
                    <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        Running Backtest...
                    </>
                ) : (
                    <>
                        <Play className="w-4 h-4" />
                        Run Backtest
                    </>
                )}
            </motion.button>

            {/* Results */}
            <AnimatePresence>
                {result && (
                    <motion.div
                        className="mt-6 grid grid-cols-2 gap-3"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                    >
                        <ResultCard
                            label="Win Rate"
                            value={`${result.winRate}%`}
                            isPositive={result.winRate > 50}
                        />
                        <ResultCard
                            label="Total Return"
                            value={`${result.totalReturn > 0 ? '+' : ''}${result.totalReturn}%`}
                            isPositive={result.totalReturn > 0}
                        />
                        <ResultCard
                            label="Total Trades"
                            value={result.trades.toString()}
                            isPositive={true}
                        />
                        <ResultCard
                            label="Max Drawdown"
                            value={`-${result.maxDrawdown}%`}
                            isPositive={result.maxDrawdown < 10}
                        />
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

function ResultCard({ label, value, isPositive }: { label: string; value: string; isPositive: boolean }) {
    return (
        <motion.div
            className="glass-card p-3 text-center"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 300 }}
        >
            <div className={`text-lg font-bold font-mono ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                {isPositive ? <TrendingUp className="w-4 h-4 inline mr-1" /> : <TrendingDown className="w-4 h-4 inline mr-1" />}
                {value}
            </div>
            <div className="text-xs text-foreground-muted">{label}</div>
        </motion.div>
    );
}
