'use client';

import { useState } from 'react';
import { 
  BarChart3, TrendingUp, Users, ShoppingCart, Percent, Calendar, 
  CheckCircle2, AlertTriangle, Play, HelpCircle, ShieldCheck, 
  TrendingDown, ArrowRight, RefreshCw, MessageSquare, Database, 
  Sparkles, Send, Dna, Calculator, Filter 
} from 'lucide-react';

interface InteractiveDashboardProps {
  slug: string;
}

export default function InteractiveDashboard({ slug }: InteractiveDashboardProps) {
  // ==========================================
  // 1. Analisis Sentimen RUU TNI State
  // ==========================================
  const [tniInput, setTniInput] = useState<string>('Revisi UU TNI mengancam supremasi sipil dan menghidupkan kembali dwifungsi militer.');
  const [tniResult, setTniResult] = useState<{
    label: 'Negatif' | 'Positif' | 'Netral';
    score: number;
    tokens: string[];
    stemmed: string[];
  }>({
    label: 'Negatif',
    score: 94.2,
    tokens: ['revisi', 'uu', 'tni', 'mengancam', 'supremasi', 'sipil', 'dan', 'menghidupkan', 'kembali', 'dwifungsi', 'militer'],
    stemmed: ['revisi', 'uu', 'tni', 'ancam', 'supremasi', 'sipil', 'hidup', 'kembali', 'dwifungsi', 'militer']
  });
  const [tniAnalyzing, setTniAnalyzing] = useState<boolean>(false);

  const handleTniAnalyze = (text: string) => {
    setTniAnalyzing(true);
    setTimeout(() => {
      let label: 'Negatif' | 'Positif' | 'Netral' = 'Netral';
      let score = 50.0;
      
      const lowerText = text.toLowerCase();
      if (lowerText.includes('ancam') || lowerText.includes('dwifungsi') || lowerText.includes('tolak') || lowerText.includes('khawatir') || lowerText.includes('orba') || lowerText.includes('mundur') || lowerText.includes('salah')) {
        label = 'Negatif';
        score = 80 + Math.random() * 18;
      } else if (lowerText.includes('dukung') || lowerText.includes('profesional') || lowerText.includes('maju') || lowerText.includes('kedaulatan') || lowerText.includes('nkri') || lowerText.includes('modernisasi') || lowerText.includes('bagus')) {
        label = 'Positif';
        score = 75 + Math.random() * 20;
      } else {
        label = 'Netral';
        score = 60 + Math.random() * 25;
      }

      // Simple tokenization & mock stemming
      const cleanText = lowerText.replace(/[^a-zA-Z0-9\s]/g, '');
      const tokens = cleanText.split(/\s+/).filter(t => t.length > 0);
      const stemmed = tokens.map(t => {
        if (t.startsWith('meng')) return t.slice(4);
        if (t.startsWith('men')) return t.slice(3);
        if (t.startsWith('me')) return t.slice(2);
        if (t.endsWith('kan')) return t.slice(0, -3);
        if (t.endsWith('an')) return t.slice(0, -2);
        return t;
      });

      setTniResult({ label, score: parseFloat(score.toFixed(1)), tokens, stemmed });
      setTniAnalyzing(false);
    }, 800);
  };

  // ==========================================
  // 2. toko_online State
  // ==========================================
  const [cart, setCart] = useState<Array<{ id: number; name: string; price: number; qty: number; stock: number }>>([
    { id: 1, name: 'Sepatu Sneakers Casual', price: 400000, qty: 1, stock: 5 },
    { id: 2, name: 'Kaos Katun Premium', price: 150000, qty: 2, stock: 10 },
    { id: 3, name: 'Jaket Bomber Slimfit', price: 350000, qty: 0, stock: 3 },
  ]);
  const [coupon, setCoupon] = useState<string>('');
  const [discountPercent, setDiscountPercent] = useState<number>(0);
  const [sqlLog, setSqlLog] = useState<string[]>([]);
  const [checkoutStep, setCheckoutStep] = useState<'idle' | 'success'>('idle');

  const updateCartQty = (id: number, delta: number) => {
    setCart(prev => prev.map(item => {
      if (item.id === id) {
        const newQty = Math.max(0, Math.min(item.stock, item.qty + delta));
        return { ...item, qty: newQty };
      }
      return item;
    }));
  };

  const applyCoupon = () => {
    if (coupon.toUpperCase() === 'DISKON10') {
      setDiscountPercent(10);
    } else {
      setDiscountPercent(0);
      alert('Kupon tidak valid. Coba masukkan: DISKON10');
    }
  };

  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  const discountAmount = (subtotal * discountPercent) / 100;
  const totalBill = subtotal - discountAmount;

  const handleCheckout = () => {
    if (subtotal === 0) return;
    
    // Simulate SQL transactions logs
    const logs = [
      '-- START TRANSACTION (Autocommit OFF)',
      'BEGIN;',
      'INSERT INTO orders (user_id, total_price, status) VALUES (42, ' + totalBill + ", 'pending');",
      'SELECT LAST_INSERT_ID() AS order_id; -- returns #10087'
    ];

    cart.forEach(item => {
      if (item.qty > 0) {
        logs.push(`-- Check stock for item ID ${item.id}`);
        logs.push(`SELECT stock FROM products WHERE id = ${item.id} FOR UPDATE; -- returns ${item.stock}`);
        logs.push(`INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (10087, ${item.id}, ${item.qty}, ${item.price});`);
        logs.push(`UPDATE products SET stock = stock - ${item.qty} WHERE id = ${item.id}; -- stock updated`);
      }
    });

    logs.push('COMMIT; -- Transaction successful, locks released.');
    
    setSqlLog(logs);
    setCheckoutStep('success');
  };

  // ==========================================
  // 3. Klasifikasi Diabetes DNA State
  // ==========================================
  const presetSequences = {
    normal: 'ATG-CGA-TTC-GGA-CTA-GCT-AAC-GCT-GCA',
    mutant: 'ATG-CGA-TTT-GCA-CTA-GCT-AAC-GCT-GCA',
    custom: 'ATG-CGA-TTC-GGA-CTA-GCT-AAC-GCT-GCA'
  };
  const [dnaSeq, setDnaSeq] = useState<string>(presetSequences.normal);
  const [dnaResult, setDnaResult] = useState<{
    label: 'Normal' | 'Risiko Diabetes Tipe 2';
    distance: number;
    kmers: string[];
  }>({
    label: 'Normal',
    distance: 0.12,
    kmers: ['ATG', 'TGC', 'GCG', 'CGA', 'GAT', 'ATT', 'TTC', 'TCG', 'CGG', 'GGA', 'GAC', 'ACT', 'CTA', 'TAG', 'AGC', 'GCT', 'CTA', 'TAA', 'AAC', 'ACG', 'CGC', 'GCT', 'CTG', 'TGC', 'GCA']
  });
  const [dnaRunning, setDnaRunning] = useState<boolean>(false);

  const runDnaClassifier = (sequence: string) => {
    setDnaRunning(true);
    setTimeout(() => {
      const cleanSeq = sequence.toUpperCase().replace(/[^ATCG]/g, '');
      
      // Calculate 3-mers
      const kmersList: string[] = [];
      for (let i = 0; i < cleanSeq.length - 2; i++) {
        kmersList.push(cleanSeq.slice(i, i + 3));
      }

      // Simple prediction: if sequence contains TTT or GCA, mark as high risk
      const hasMutations = cleanSeq.includes('TTT') || cleanSeq.includes('GCA') || cleanSeq.includes('TTA');
      const label = hasMutations ? 'Risiko Diabetes Tipe 2' : 'Normal';
      const distance = hasMutations ? 1.45 + Math.random() * 0.5 : 0.08 + Math.random() * 0.15;

      setDnaResult({
        label,
        distance: parseFloat(distance.toFixed(3)),
        kmers: kmersList.slice(0, 25)
      });
      setDnaRunning(false);
    }, 700);
  };

  // ==========================================
  // 4. CS-AI-Agent State
  // ==========================================
  const [csInput, setCsInput] = useState<string>('ORD-9921: Paket saya belum sampai dari kemarin. Saya mau refund!');
  const [csConversation, setCsConversation] = useState<Array<{ sender: 'user' | 'agent'; text: string }>>([
    { sender: 'user', text: 'Halo, saya ingin menanyakan status pesanan saya.' },
    { sender: 'agent', text: 'Halo! Tentu, boleh saya minta nomor pesanan (Order ID) Anda untuk saya lacak?' },
  ]);
  const [agentLogs, setAgentLogs] = useState<string[]>([]);
  const [csLoading, setCsLoading] = useState<boolean>(false);

  const runAgentResponse = (message: string) => {
    if (!message.trim()) return;

    setCsConversation(prev => [...prev, { sender: 'user', text: message }]);
    setCsLoading(true);

    setTimeout(() => {
      let reply = '';
      const logs = [
        `[Agent Initiated] Parsing message: "${message}"`,
        `[Step 1: NLP Intent Detection] Mapped query to Intent: 'Order Status Query' / 'Refund Request'`,
      ];

      const lower = message.toLowerCase();
      if (lower.includes('ord') || lower.includes('paket') || lower.includes('lacak')) {
        logs.push(`[Step 2: Tool Selection] Message requires database lookup. Selected tool: 'TrackPackage'`);
        logs.push(`[Step 3: Action Execution] Calling TrackPackage(order_id="ORD-9921")...`);
        logs.push(`[Step 4: Observation] Database returned: { status: 'Transit', location: 'Jakarta Barat', carrier: 'JNE Express', status_code: 3 }`);
        
        if (lower.includes('refund')) {
          logs.push(`[Step 5: Policy Check] Selected tool: 'RefundPolicy'`);
          logs.push(`[Step 6: Action Execution] Calling RefundPolicy(status="Transit")...`);
          logs.push(`[Step 7: Observation] Policy returned: "Refund cannot be processed while item is in active transit."`);
          
          reply = 'Halo! Saya telah melacak pesanan Anda dengan nomor ORD-9921. Saat ini paket sedang transit di pusat sortir Jakarta Barat JNE Express. Berdasarkan kebijakan e-commerce, kami tidak dapat memproses pengembalian dana (refund) untuk barang yang sedang dalam proses pengantaran aktif. Mohon ditunggu hingga kurir sampai ke alamat Anda ya.';
        } else {
          reply = 'Halo! Saya melacak pesanan ORD-9921 Anda. Paket Anda saat ini berada di pusat sortir Jakarta Barat JNE Express dan sedang menuju ke alamat pengiriman Anda. Estimasi sampai hari ini.';
        }
      } else {
        logs.push(`[Step 2: Direct Reply] No external database tool needed. Categorized as general greeting.`);
        reply = 'Halo! Ada yang bisa saya bantu terkait pesanan, katalog produk, atau penawaran promo hari ini?';
      }

      logs.push(`[Step 8: Output Synthesis] Generating empathetic tone response.`);
      setAgentLogs(logs);
      setCsConversation(prev => [...prev, { sender: 'agent', text: reply }]);
      setCsLoading(false);
    }, 1200);
  };

  // ==========================================
  // 5. avg-down-idx State
  // ==========================================
  const [stockCode, setStockCode] = useState<string>('BBRI');
  const [initialShares, setInitialShares] = useState<number>(100); // 100 Lots
  const [initialPrice, setInitialPrice] = useState<number>(6000); // Rp6,000 / share
  const [newShares, setNewShares] = useState<number>(200); // Buy 200 more Lots
  const [newPrice, setNewPrice] = useState<number>(4200); // Buy at Rp4,200 / share
  const [currentMarketPrice, setCurrentMarketPrice] = useState<number>(4400);

  // Calculations
  const totalInitCost = initialShares * 100 * initialPrice;
  const totalNewCost = newShares * 100 * newPrice;
  const totalCost = totalInitCost + totalNewCost;
  const totalSharesQty = (initialShares + newShares) * 100;
  const combinedAvgPrice = Math.round(totalCost / totalSharesQty);
  
  const initValue = initialShares * 100 * currentMarketPrice;
  const combinedValue = totalSharesQty * currentMarketPrice;
  
  const floatingLossInit = initValue - totalInitCost;
  const floatingLossCombined = combinedValue - totalCost;
  const lossPercentInit = ((floatingLossInit) / totalInitCost) * 100;
  const lossPercentCombined = ((floatingLossCombined) / totalCost) * 100;

  const requiredRiseInit = ((initialPrice - currentMarketPrice) / currentMarketPrice) * 100;
  const requiredRiseCombined = ((combinedAvgPrice - currentMarketPrice) / currentMarketPrice) * 100;

  // ==========================================
  // 6. data-saham-indonesia State
  // ==========================================
  const [peFilter, setPeFilter] = useState<number>(18);
  const [pbvFilter, setPbvFilter] = useState<number>(2.5);
  const [minRoe, setMinRoe] = useState<boolean>(true);

  const stockList = [
    { ticker: 'BBRI', name: 'Bank Rakyat Indonesia', pe: 10.5, pbv: 2.1, roe: 22.7, yield: 6.2, price: 4300, status: 'Undervalued' },
    { ticker: 'TLKM', name: 'Telkom Indonesia', pe: 14.5, pbv: 2.3, roe: 14.6, yield: 5.1, price: 3200, status: 'Fair Value' },
    { ticker: 'ASII', name: 'Astra International', pe: 8.8, pbv: 1.1, roe: 12.8, yield: 7.2, price: 5100, status: 'Undervalued' },
    { ticker: 'GOTO', name: 'GoTo Gojek Tokopedia', pe: -5.2, pbv: 0.7, roe: -14.1, yield: 0.0, price: 62, status: 'Loss Making' },
    { ticker: 'UNVR', name: 'Unilever Indonesia', pe: 20.0, pbv: 6.2, roe: 31.1, yield: 5.8, price: 2800, status: 'Overvalued' },
    { ticker: 'SMGR', name: 'Semen Indonesia', pe: 11.2, pbv: 0.9, roe: 8.2, yield: 4.8, price: 3900, status: 'Undervalued' },
    { ticker: 'ICBP', name: 'Indofood CBP', pe: 16.2, pbv: 2.8, roe: 18.5, yield: 3.4, price: 10800, status: 'Fair Value' },
  ];

  const filteredStocks = stockList.filter(s => {
    const passPe = s.pe > 0 && s.pe <= peFilter;
    const passPbv = s.pbv <= pbvFilter;
    const passRoe = minRoe ? s.roe >= 10 : true;
    return passPe && passPbv && passRoe;
  });


  // ----------------------------------------------------
  // RENDER 1: Analisis Sentimen RUU TNI
  // ----------------------------------------------------
  if (slug === 'analisis-sentimen-ruu-tni') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-indigo-400">
              <MessageSquare className="w-5 h-5" /> NLP Sentimen RUU TNI Simulator
            </h4>
            <p className="text-xs text-slate-400">Preprocessing Text Bahasa Indonesia & Model Naive Bayes</p>
          </div>
          <span className="text-[10px] font-mono bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded border border-indigo-500/20">
            Jupyter Notebook API
          </span>
        </div>

        {/* Form Input */}
        <div className="mb-6">
          <label className="text-xs text-slate-300 font-semibold block mb-2">Input Komentar/Tweet:</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={tniInput}
              onChange={(e) => setTniInput(e.target.value)}
              className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sm focus:outline-none focus:border-indigo-500 text-slate-100"
            />
            <button
              onClick={() => handleTniAnalyze(tniInput)}
              disabled={tniAnalyzing}
              className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 font-semibold text-sm transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {tniAnalyzing ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              Analisis
            </button>
          </div>
          
          <div className="flex flex-wrap gap-2 mt-3">
            <span className="text-xs text-slate-400">Preset contoh:</span>
            <button 
              onClick={() => {
                const text = "Tolak dwifungsi TNI! Jangan kembalikan militer ke masa Orde Baru.";
                setTniInput(text);
                handleTniAnalyze(text);
              }}
              className="text-[11px] bg-slate-900 border border-slate-800 hover:border-slate-700 px-2.5 py-1 rounded-md text-slate-300 transition-colors cursor-pointer"
            >
              Kritik (Negatif)
            </button>
            <button 
              onClick={() => {
                const text = "Dukung modernisasi alutsista TNI untuk pertahanan kedaulatan NKRI yang lebih kuat.";
                setTniInput(text);
                handleTniAnalyze(text);
              }}
              className="text-[11px] bg-slate-900 border border-slate-800 hover:border-slate-700 px-2.5 py-1 rounded-md text-slate-300 transition-colors cursor-pointer"
            >
              Dukungan (Positif)
            </button>
          </div>
        </div>

        {/* Results layout */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Preprocessing Steps */}
          <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4">
            <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
              <RefreshCw className="w-3.5 h-3.5 text-indigo-400" /> Tahapan Preprocessing
            </span>
            
            <div className="space-y-3.5 text-xs">
              <div>
                <span className="text-slate-400 block mb-1">1. Tokenisasi (Pemisahan Kata):</span>
                <div className="flex flex-wrap gap-1">
                  {tniResult.tokens.map((t, idx) => (
                    <span key={idx} className="bg-slate-950 border border-slate-800 px-1.5 py-0.5 rounded font-mono text-[10px]">
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              <div className="border-t border-slate-800/60 pt-3">
                <span className="text-slate-400 block mb-1">2. Stemming Sastrawi (Kata Dasar):</span>
                <div className="flex flex-wrap gap-1">
                  {tniResult.stemmed.map((t, idx) => (
                    <span key={idx} className="bg-indigo-950/20 border border-indigo-900/40 text-indigo-300 px-1.5 py-0.5 rounded font-mono text-[10px]">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Model Inference */}
          <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
                <BarChart3 className="w-3.5 h-3.5 text-indigo-400" /> Naive Bayes Inference
              </span>

              <div className="flex items-center gap-4 my-2">
                <div className={`text-center py-3 px-5 rounded-2xl border font-black text-lg ${
                  tniResult.label === 'Negatif' 
                    ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' 
                    : tniResult.label === 'Positif' 
                      ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                      : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
                }`}>
                  {tniResult.label}
                </div>
                <div>
                  <span className="text-slate-400 text-xs block font-semibold">Tingkat Keyakinan</span>
                  <span className="text-2xl font-black text-slate-100">{tniResult.score}%</span>
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800/60 pt-3 text-[11px] text-slate-400 leading-relaxed">
              <strong>Catatan Model:</strong> Fitur TF-IDF memetakan pembobotan kata. Kata kunci negatif seperti <em>dwifungsi</em> dan <em>orba</em> memberikan kontribusi bobot posterior yang sangat tinggi ke arah label Negatif.
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER 2: toko_online (PHP / MySQL)
  // ----------------------------------------------------
  if (slug === 'toko-online') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-emerald-400">
              <ShoppingCart className="w-5 h-5" /> PHP Checkout & Transaction Simulator
            </h4>
            <p className="text-xs text-slate-400">Cart, Stock Verification, and ACID SQL Commit Control</p>
          </div>
          <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded border border-emerald-500/20">
            MySQL Transaction
          </span>
        </div>

        {checkoutStep === 'idle' ? (
          <div className="grid md:grid-cols-2 gap-6">
            {/* Catalog & Cart */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
              <h5 className="text-xs font-bold text-slate-300 mb-3 block uppercase tracking-wider">Keranjang Belanja</h5>
              <div className="space-y-3">
                {cart.map((item) => (
                  <div key={item.id} className="flex justify-between items-center bg-slate-950 p-3 rounded-lg border border-slate-800/60">
                    <div>
                      <span className="text-xs font-bold block text-slate-100">{item.name}</span>
                      <span className="text-[11px] text-slate-400">Rp {item.price.toLocaleString('id-ID')} (Stok: {item.stock})</span>
                    </div>
                    <div className="flex items-center gap-2.5">
                      <button 
                        onClick={() => updateCartQty(item.id, -1)}
                        className="w-6 h-6 rounded-full bg-slate-900 border border-slate-800 text-xs font-bold hover:bg-slate-800 flex items-center justify-center cursor-pointer"
                      >
                        -
                      </button>
                      <span className="text-xs font-bold font-mono w-4 text-center">{item.qty}</span>
                      <button 
                        onClick={() => updateCartQty(item.id, 1)}
                        className="w-6 h-6 rounded-full bg-slate-900 border border-slate-800 text-xs font-bold hover:bg-slate-800 flex items-center justify-center cursor-pointer"
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Calculations & Checkout */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
              <div>
                <h5 className="text-xs font-bold text-slate-300 mb-3 block uppercase tracking-wider">Ringkasan Pembayaran</h5>
                <div className="space-y-2 text-xs mb-4">
                  <div className="flex justify-between text-slate-400">
                    <span>Subtotal:</span>
                    <span>Rp {subtotal.toLocaleString('id-ID')}</span>
                  </div>
                  
                  {/* Coupon Area */}
                  <div className="py-2 border-t border-b border-slate-850 my-2 flex gap-2">
                    <input
                      type="text"
                      placeholder="Kupon (DISKON10)"
                      value={coupon}
                      onChange={(e) => setCoupon(e.target.value)}
                      className="flex-1 px-3 py-1 rounded bg-slate-950 border border-slate-800 text-xs text-slate-200"
                    />
                    <button 
                      onClick={applyCoupon}
                      className="px-2.5 py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[11px] rounded font-semibold cursor-pointer"
                    >
                      Terapkan
                    </button>
                  </div>

                  {discountAmount > 0 && (
                    <div className="flex justify-between text-emerald-400 font-semibold">
                      <span>Kupon Diskon (10%):</span>
                      <span>- Rp {discountAmount.toLocaleString('id-ID')}</span>
                    </div>
                  )}

                  <div className="flex justify-between text-sm font-black text-slate-100 border-t border-slate-800 pt-2">
                    <span>Total Tagihan:</span>
                    <span>Rp {totalBill.toLocaleString('id-ID')}</span>
                  </div>
                </div>
              </div>

              <button
                onClick={handleCheckout}
                disabled={subtotal === 0}
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 font-bold text-sm text-white rounded-xl transition-all cursor-pointer disabled:opacity-40"
              >
                Checkout & Simpan Order
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Checkout Success Message */}
            <div className="bg-emerald-950/20 border border-emerald-900/50 p-4 rounded-xl flex items-center gap-3">
              <CheckCircle2 className="w-6 h-6 text-emerald-400 shrink-0" />
              <div>
                <h5 className="text-sm font-bold text-emerald-400">Transaksi Checkout Berhasil!</h5>
                <p className="text-xs text-slate-300">MySQL Transaction successfully committed. Stok produk telah dikurangi otomatis.</p>
              </div>
              <button 
                onClick={() => {
                  setCheckoutStep('idle');
                  setSqlLog([]);
                }}
                className="ml-auto px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs font-semibold cursor-pointer"
              >
                Belanja Lagi
              </button>
            </div>

            {/* SQL Transaction Log */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-xs font-bold text-slate-300 flex items-center gap-2 mb-3">
                <Database className="w-4 h-4 text-emerald-400" /> Database Relational Transaction Logs (ACID)
              </span>
              <pre className="text-[10px] font-mono text-emerald-300/90 leading-normal p-3 rounded-lg bg-slate-950 overflow-x-auto max-h-48 whitespace-pre-wrap">
                {sqlLog.join('\n')}
              </pre>
            </div>
          </div>
        )}
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER 3: Klasifikasi Diabetes DNA (Math / Bioinfo)
  // ----------------------------------------------------
  if (slug === 'klasifikasi-diabetes-dna') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-cyan-400">
              <Dna className="w-5 h-5" /> DNA Sequence Diabetes Classifier
            </h4>
            <p className="text-xs text-slate-400">Bioinformatics 3-mers Frequency Vector & KNN Distance Model</p>
          </div>
          <span className="text-[10px] font-mono bg-cyan-500/10 text-cyan-400 px-2 py-1 rounded border border-cyan-500/20">
            K-mers & KNN
          </span>
        </div>

        <div className="mb-6">
          <label className="text-xs text-slate-300 font-semibold block mb-2">Input Sekuens Genomik DNA (A, T, C, G):</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={dnaSeq}
              onChange={(e) => setDnaSeq(e.target.value.toUpperCase().replace(/[^ATCG-]/g, ''))}
              className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sm focus:outline-none focus:border-cyan-500 text-slate-100 font-mono tracking-wider"
            />
            <button
              onClick={() => runDnaClassifier(dnaSeq)}
              disabled={dnaRunning}
              className="px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-700 font-semibold text-sm transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {dnaRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              Scan DNA
            </button>
          </div>

          <div className="flex flex-wrap gap-2 mt-3">
            <span className="text-xs text-slate-400">Varian Uji:</span>
            <button 
              onClick={() => {
                setDnaSeq(presetSequences.normal);
                runDnaClassifier(presetSequences.normal);
              }}
              className="text-[11px] bg-slate-900 border border-slate-800 hover:border-slate-700 px-2.5 py-1 rounded-md text-slate-300 transition-colors cursor-pointer"
            >
              Sequence Normal (Sehat)
            </button>
            <button 
              onClick={() => {
                setDnaSeq(presetSequences.mutant);
                runDnaClassifier(presetSequences.mutant);
              }}
              className="text-[11px] bg-slate-900 border border-slate-800 hover:border-slate-700 px-2.5 py-1 rounded-md text-slate-300 transition-colors cursor-pointer"
            >
              Sequence Mutant (Risiko Diabetes)
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Vectorized output */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
            <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
              <Dna className="w-3.5 h-3.5 text-cyan-400" /> Ekstraksi Substring 3-mers
            </span>
            <div className="max-h-36 overflow-y-auto p-2 bg-slate-950 rounded-lg border border-slate-900">
              <div className="flex flex-wrap gap-1.5">
                {dnaResult.kmers.map((kmer, idx) => (
                  <span key={idx} className="text-[10px] font-mono bg-cyan-950/20 text-cyan-300 px-2 py-0.5 rounded border border-cyan-900/30">
                    {kmer}
                  </span>
                ))}
              </div>
            </div>
            <p className="text-[10px] text-slate-400 mt-3">
              Masing-masing 3-mers dihitung frekuensi kemunculannya untuk membentuk profil matriks densitas 64-dimensi.
            </p>
          </div>

          {/* Model classification */}
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" /> Hasil Klasifikasi Genom
              </span>
              
              <div className="flex items-center gap-4 my-2">
                <div className={`text-center py-3 px-4 rounded-xl border font-black text-sm ${
                  dnaResult.label === 'Normal' 
                    ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
                    : 'bg-rose-500/10 border-rose-500/20 text-rose-400 animate-pulse'
                }`}>
                  {dnaResult.label}
                </div>
                <div>
                  <span className="text-slate-400 text-xs block font-semibold">Euclidean Distance</span>
                  <span className="text-xl font-bold text-slate-100">{dnaResult.distance}</span>
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800/60 pt-3 text-[10px] text-slate-400 leading-normal">
              <strong>Formula Jarak:</strong> Jika jarak Euclidean terhadap klaster rujukan risiko tinggi &lt; threshold, DNA diklasifikasikan sebagai pembawa genetik diabetes tipe 2.
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER 4: CS-AI-Agent Customer Service
  // ----------------------------------------------------
  if (slug === 'cs-ai-agent') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-violet-400">
              <Sparkles className="w-5 h-5" /> CS AI Agent Interaction Terminal
            </h4>
            <p className="text-xs text-slate-400">ReAct Framework reasoning loop: Thought, Action, Observation, Answer</p>
          </div>
          <span className="text-[10px] font-mono bg-violet-500/10 text-violet-400 px-2 py-1 rounded border border-violet-500/20">
            LangChain & OpenAI
          </span>
        </div>

        <div className="grid md:grid-cols-5 gap-6">
          {/* Chat Window (3 cols) */}
          <div className="md:col-span-3 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between h-[360px]">
            {/* Header chat */}
            <div className="flex items-center gap-2 border-b border-slate-850 pb-2 mb-3">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
              <span className="text-xs font-bold text-slate-200">Customer Support Chatbot</span>
            </div>

            {/* Chat Bubble history */}
            <div className="flex-1 overflow-y-auto space-y-3.5 pr-2 mb-4 scrollbar-thin">
              {csConversation.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-2xl max-w-[85%] text-xs leading-relaxed ${
                    msg.sender === 'user' 
                      ? 'bg-violet-600 text-white rounded-tr-none' 
                      : 'bg-slate-950 text-slate-200 rounded-tl-none border border-slate-850'
                  }`}>
                    {msg.text}
                  </div>
                </div>
              ))}
              {csLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-950 p-3 rounded-2xl rounded-tl-none border border-slate-850 text-xs text-slate-400 flex items-center gap-2">
                    <RefreshCw className="w-3.5 h-3.5 animate-spin text-violet-400" /> Agen sedang berpikir...
                  </div>
                </div>
              )}
            </div>

            {/* Send console */}
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Kirim keluhan (misal: Cek paket ORD-9921)"
                value={csInput}
                onChange={(e) => setCsInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') { runAgentResponse(csInput); setCsInput(''); } }}
                className="flex-1 px-3 py-2 rounded-xl bg-slate-950 border border-slate-850 text-xs text-slate-200 focus:outline-none"
              />
              <button 
                onClick={() => { runAgentResponse(csInput); setCsInput(''); }}
                className="p-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-white cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Reasoning trace logs (2 cols) */}
          <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col h-[360px] justify-between">
            <div>
              <span className="text-xs font-bold text-slate-300 block mb-2 flex items-center gap-1.5">
                <Database className="w-4 h-4 text-violet-400" /> LLM Execution Trace
              </span>
              <p className="text-[10px] text-slate-400 mb-3">Lihat proses bagaimana Agen AI melakukan reasoning di belakang layar.</p>
            </div>

            <div className="flex-1 bg-slate-950 p-2.5 rounded-lg border border-slate-850 overflow-y-auto max-h-60 font-mono text-[9px] text-violet-300/95 leading-relaxed space-y-2.5">
              {agentLogs.length === 0 ? (
                <div className="text-slate-500 text-center py-12">Belum ada panggilan tools. Coba kirim pesan keluhan di panel chat.</div>
              ) : (
                agentLogs.map((log, idx) => (
                  <div key={idx} className="border-b border-slate-900/50 pb-1.5">
                    {log}
                  </div>
                ))
              )}
            </div>

            <div className="text-[9px] text-slate-500 border-t border-slate-850 pt-2.5 mt-2">
              <strong>Teknologi:</strong> Kerangka ReAct mendikte agen untuk menulis "Thought" terlebih dulu sebelum memicu "Action" alat.
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER 5: Kalkulator Average Down Saham IDX
  // ----------------------------------------------------
  if (slug === 'avg-down-idx') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-cyan-400">
              <Calculator className="w-5 h-5" /> IDX Stock Average Down Calculator
            </h4>
            <p className="text-xs text-slate-400">Simulasikan Penurunan Rata-rata Beli untuk Pemulihan Modal Lebih Cepat</p>
          </div>
          <span className="text-[10px] font-mono bg-cyan-500/10 text-cyan-400 px-2 py-1 rounded border border-cyan-500/20">
            TypeScript Math
          </span>
        </div>

        {/* Inputs */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
            <span className="text-[11px] text-slate-400 font-bold block mb-2">1. Kepemilikan Awal</span>
            <div className="space-y-2">
              <div>
                <label className="text-[10px] text-slate-500 block">Jumlah Saham (Lot):</label>
                <input
                  type="number"
                  value={initialShares}
                  onChange={(e) => setInitialShares(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200"
                />
              </div>
              <div>
                <label className="text-[10px] text-slate-500 block">Harga Beli Awal (Rp):</label>
                <input
                  type="number"
                  value={initialPrice}
                  onChange={(e) => setInitialPrice(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200"
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
            <span className="text-[11px] text-slate-400 font-bold block mb-2">2. Pembelian Rencana</span>
            <div className="space-y-2">
              <div>
                <label className="text-[10px] text-slate-500 block">Saham Baru (Lot):</label>
                <input
                  type="number"
                  value={newShares}
                  onChange={(e) => setNewShares(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200"
                />
              </div>
              <div>
                <label className="text-[10px] text-slate-500 block">Harga Beli Baru (Rp):</label>
                <input
                  type="number"
                  value={newPrice}
                  onChange={(e) => setNewPrice(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200"
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
            <span className="text-[11px] text-slate-400 font-bold block mb-2">3. Kondisi Pasar</span>
            <div className="space-y-2">
              <div>
                <label className="text-[10px] text-slate-500 block">Kode Saham (Ticker):</label>
                <select 
                  value={stockCode}
                  onChange={(e) => setStockCode(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200 focus:outline-none"
                >
                  <option value="BBRI">BBRI</option>
                  <option value="TLKM">TLKM</option>
                  <option value="ASII">ASII</option>
                </select>
              </div>
              <div>
                <label className="text-[10px] text-slate-500 block">Harga Pasar Saat Ini (Rp):</label>
                <input
                  type="number"
                  value={currentMarketPrice}
                  onChange={(e) => setCurrentMarketPrice(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 px-2 py-1 rounded text-xs text-slate-200"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Results comparisons */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
            <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
              <TrendingDown className="w-4 h-4 text-rose-400" /> Perbandingan Sebelum vs Sesudah Average Down
            </span>
            <div className="space-y-3.5 text-xs">
              <div className="flex justify-between border-b border-slate-850 pb-2">
                <span className="text-slate-400">Harga Rata-rata Beli:</span>
                <span className="font-semibold text-slate-300">
                  Rp {initialPrice.toLocaleString('id-ID')} → <strong className="text-cyan-400">Rp {combinedAvgPrice.toLocaleString('id-ID')}</strong>
                </span>
              </div>
              <div className="flex justify-between border-b border-slate-850 pb-2">
                <span className="text-slate-400">Total Saham Dipegang:</span>
                <span className="font-mono text-slate-300">
                  {initialShares} Lot → <strong>{initialShares + newShares} Lot</strong>
                </span>
              </div>
              <div className="flex justify-between border-b border-slate-850 pb-2">
                <span className="text-slate-400">Floating Loss Real:</span>
                <span className="font-mono text-slate-300">
                  Rp {floatingLossInit.toLocaleString('id-ID')} ({lossPercentInit.toFixed(1)}%) → <strong className={floatingLossCombined <= floatingLossInit ? 'text-emerald-400' : 'text-rose-400'}>
                    Rp {floatingLossCombined.toLocaleString('id-ID')} ({lossPercentCombined.toFixed(1)}%)
                  </strong>
                </span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold text-slate-300 block mb-3 flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4 text-cyan-400" /> Target Rise Kenaikan ke Break-Even (Kembali Modal)
              </span>
              <div className="grid grid-cols-2 gap-4 text-center my-1">
                <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                  <span className="text-[10px] text-slate-500 block">Kenaikan Awal</span>
                  <span className="text-lg font-black text-rose-400">{requiredRiseInit.toFixed(1)}%</span>
                </div>
                <div className="p-3 rounded-lg bg-cyan-950/20 border border-cyan-900/30">
                  <span className="text-[10px] text-slate-500 block">Kenaikan Gabungan</span>
                  <span className="text-lg font-black text-emerald-400">{requiredRiseCombined.toFixed(1)}%</span>
                </div>
              </div>
            </div>

            <div className="text-[10px] text-slate-400 border-t border-slate-850 pt-2.5">
              <strong>Simulasi Insight:</strong> Dengan membeli lot tambahan di bawah, target kenaikan harga pasar agar portofolio kembali impas/break-even turun sebesar <strong>{(requiredRiseInit - requiredRiseCombined).toFixed(1)}%</strong>!
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER 6: Data Pipeline Saham Indonesia
  // ----------------------------------------------------
  if (slug === 'data-saham-indonesia') {
    return (
      <div className="glass-card p-6 bg-slate-950 text-slate-100 border-slate-800 rounded-2xl w-full">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
          <div>
            <h4 className="text-lg font-bold flex items-center gap-2 text-indigo-400">
              <Filter className="w-5 h-5" /> IDX Fundamental Stock Screener
            </h4>
            <p className="text-xs text-slate-400">Scraped data filter pipeline by financial metrics (PE, PBV, and ROE)</p>
          </div>
          <span className="text-[10px] font-mono bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded border border-indigo-500/20">
            Pandas pipeline
          </span>
        </div>

        {/* Dynamic Controls */}
        <div className="grid md:grid-cols-3 gap-4 mb-6 bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div>
            <div className="flex justify-between text-xs mb-1.5">
              <span className="text-slate-400 font-semibold">PE Ratio Maksimal:</span>
              <span className="text-indigo-400 font-bold font-mono">{peFilter}x</span>
            </div>
            <input
              type="range"
              min="5"
              max="25"
              value={peFilter}
              onChange={(e) => setPeFilter(parseInt(e.target.value))}
              className="w-full accent-indigo-500 h-1.5 bg-slate-950 rounded-lg cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1.5">
              <span className="text-slate-400 font-semibold">PBV Ratio Maksimal:</span>
              <span className="text-indigo-400 font-bold font-mono">{pbvFilter}x</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="5.0"
              step="0.1"
              value={pbvFilter}
              onChange={(e) => setPbvFilter(parseFloat(e.target.value))}
              className="w-full accent-indigo-500 h-1.5 bg-slate-950 rounded-lg cursor-pointer"
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-semibold">Batas Minimum ROE &ge; 10%:</span>
            <button
              onClick={() => setMinRoe(!minRoe)}
              className={`w-11 h-6 rounded-full p-1 cursor-pointer transition-colors ${
                minRoe ? 'bg-indigo-600' : 'bg-slate-800'
              }`}
            >
              <div
                className={`w-4 h-4 rounded-full bg-white transition-transform ${
                  minRoe ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Output Table */}
        <div className="bg-slate-900 border border-slate-850 rounded-xl overflow-hidden">
          <div className="overflow-x-auto max-h-56">
            <table className="w-full text-xs text-left text-slate-300">
              <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-850">
                <tr>
                  <th className="px-4 py-2.5">Kode</th>
                  <th className="px-4 py-2.5">Nama Emiten</th>
                  <th className="px-4 py-2.5 text-right">Harga (Rp)</th>
                  <th className="px-4 py-2.5 text-right">PE Ratio</th>
                  <th className="px-4 py-2.5 text-right">PBV Ratio</th>
                  <th className="px-4 py-2.5 text-right">ROE (%)</th>
                  <th className="px-4 py-2.5 text-right">Dividend Yield</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-850">
                {filteredStocks.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="text-center py-8 text-slate-500">Tidak ada emiten yang lolos filter fundamental pipeline.</td>
                  </tr>
                ) : (
                  filteredStocks.map((stock) => (
                    <tr key={stock.ticker} className="hover:bg-slate-950/40">
                      <td className="px-4 py-3 font-bold text-indigo-400">{stock.ticker}</td>
                      <td className="px-4 py-3 text-slate-200">{stock.name}</td>
                      <td className="px-4 py-3 text-right font-mono">Rp {stock.price.toLocaleString('id-ID')}</td>
                      <td className="px-4 py-3 text-right font-mono">{stock.pe}x</td>
                      <td className="px-4 py-3 text-right font-mono">{stock.pbv}x</td>
                      <td className="px-4 py-3 text-right font-mono text-emerald-400">{stock.roe}%</td>
                      <td className="px-4 py-3 text-right font-mono text-indigo-300">{stock.yield}%</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-4 text-[10px] text-slate-400 bg-slate-900 border border-slate-850 p-2.5 rounded-lg">
          <strong>Pipeline Logic:</strong> Screener di atas menyaring database hasil scraping secara real-time. Saham bernilai tinggi yang lolos kriteria adalah target utama untuk dilakukan investasi dengan teknik Value Investing.
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 border border-dashed border-slate-700 text-center rounded-xl text-slate-400 text-xs">
      Dashboard mockup tidak tersedia untuk proyek ini.
    </div>
  );
}
