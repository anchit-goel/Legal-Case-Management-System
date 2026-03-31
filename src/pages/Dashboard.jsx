import React from 'react';

const HearingRow = ({ time, period, title, location, type }) => (
    <div className="px-8 py-5 flex items-center group hover:bg-surface-container-low transition-colors">
        <div className="w-20 text-center border-r border-outline-variant/20 mr-8">
            <p className="text-xs font-bold text-on-surface-variant uppercase">{time}</p>
            <p className="text-[10px] text-slate-400 uppercase font-medium">{period}</p>
        </div>
        <div className="flex-1">
            <h4 className="font-bold text-on-surface">{title}</h4>
            <p className="text-sm text-on-surface-variant">{location}</p>
        </div>
        <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-tighter ${
                type === 'Pre-Trial' ? 'bg-primary-container text-on-primary-container' :
                type === 'Evidentiary' ? 'bg-secondary-container text-on-secondary-container' :
                'bg-tertiary-container text-on-tertiary-container'
            }`}>
                {type}
            </span>
            <button className="w-8 h-8 rounded-full flex items-center justify-center text-slate-400 group-hover:bg-white group-hover:text-primary transition-all">
                <span className="material-symbols-outlined">more_vert</span>
            </button>
        </div>
    </div>
);

const Dashboard = () => {
    return (
        <div className="pt-8 px-10 pb-12">
            <div className="mb-10 flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-extrabold text-on-surface tracking-tight leading-none mb-2">Morning, Counselor.</h2>
                    <p className="text-on-surface-variant font-medium">You have 4 hearings scheduled for today across 2 districts.</p>
                </div>
                <div className="bg-surface-container-lowest p-1 rounded-xl flex gap-1 shadow-sm">
                    <button className="px-4 py-1.5 rounded-lg text-sm font-bold bg-primary text-on-primary shadow-sm">Today</button>
                    <button className="px-4 py-1.5 rounded-lg text-sm font-medium text-on-surface-variant hover:bg-surface-container-high transition-colors">Weekly</button>
                </div>
            </div>

            <div className="grid grid-cols-12 gap-6">
                {/* Financial Cards */}
                <div className="col-span-12 lg:col-span-4 bg-surface-container-lowest p-6 rounded-xl shadow-sm border-l-4 border-primary">
                    <div className="flex justify-between items-start mb-4">
                        <span className="material-symbols-outlined text-primary bg-primary-container p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>account_balance_wallet</span>
                        <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-widest">+12% vs LY</span>
                    </div>
                    <p className="text-sm font-medium text-on-surface-variant mb-1">Total Firm Profits</p>
                    <h3 className="text-3xl font-extrabold text-on-surface">$412,850.00</h3>
                    <div className="mt-4 pt-4 border-t border-outline-variant/10">
                        <div className="w-full bg-surface-container-low h-1.5 rounded-full overflow-hidden">
                            <div className="bg-primary w-[72%] h-full rounded-full"></div>
                        </div>
                        <p className="text-[10px] mt-2 text-on-surface-variant uppercase font-bold tracking-tighter">72% of Annual Target Achieved</p>
                    </div>
                </div>

                <div className="col-span-12 lg:col-span-4 bg-surface-container-lowest p-6 rounded-xl shadow-sm border-l-4 border-secondary">
                    <div className="flex justify-between items-start mb-4">
                        <span className="material-symbols-outlined text-secondary bg-secondary-container p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>pending_actions</span>
                        <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">14 Invoices</span>
                    </div>
                    <p className="text-sm font-medium text-on-surface-variant mb-1">Fees to be Collected</p>
                    <h3 className="text-3xl font-extrabold text-on-surface">$84,200.00</h3>
                    <div className="mt-4 flex -space-x-2">
                        {[
                            "https://lh3.googleusercontent.com/aida-public/AB6AXuBkDe5qw97FHAIJUJgmuWWZzgM1uCl78YMvZHje1Tdp_BvnkRHabMmmvM07ccGeL4_aBaVysujO4u-9BwpNhtJF_bExM8EdTZ3jBVwKqWBojsO6ePw61NnFh8ZMk-cDKEGZCgBJmrICo4Q5qmtkGaKg10xX99FLxVnNexzktnjBPAgJa9MRDP-iKYzLh1Gt-2DxbXwjGGMSctl4SKZIgwDDOiyjKt5M6ArWZ9spelZ8B2cIjMOMqTzlrtlaSPptJgpjrmDTxJP80dy8",
                            "https://lh3.googleusercontent.com/aida-public/AB6AXuB18Y1yedmpus10SIL178K8qOr2YvCLqaM2GwPamERR13xvhNyJqvvgCZu6Oq7ZM16Pqj_gv7WrrM-9z72V9WzNlws-y5KsqSNy5a4fC3KHSU-3tV5ekANUbqwZ2hUFq-0N6G70NqKfcMeNljF4a_zORIDY9HkdMYRlAwlDGy-v7YHPHwr_s53ibe2RM-tLX-I__rrI4vWT8U5HdCwg5OakIjwG_h_hcMcLo7tgzV-hWqkO2RwAB8twigwc0gvr678pPbJi0PSF_eZT",
                            "https://lh3.googleusercontent.com/aida-public/AB6AXuBPXINPw3E_trmAMetap_Kw9CjPWjiQqtB8BAk_StG1uF5yyDCkANAAzuE7Yq78RC_rCBIjQUUQ6Gsk3GlnlW9HxzsubnhXINJdRCRbwkkkhQrJ3PK_Mvq8qKIJ_7Cp9iJwZN8dMsEy22oy6UZRq8A5K2HJ-E2UnoxUuEl3VSBPbQVx_I73gd70jqfPILXUw3KnTKdkEJl4lH52kIw_RkWGYkd7Dw-80-GrI2xMw_SCG4B-D6T4glto14rxnTzC_Yc2JwHTf6WXkWuR"
                        ].map((src, i) => (
                            <img key={i} className="w-7 h-7 rounded-full border-2 border-surface-container-lowest object-cover" src={src} alt="Client" />
                        ))}
                        <div className="w-7 h-7 rounded-full bg-surface-container-high border-2 border-surface-container-lowest flex items-center justify-center text-[10px] font-bold">+11</div>
                    </div>
                </div>

                <div className="col-span-12 lg:col-span-4 bg-primary text-on-primary p-6 rounded-xl shadow-lg relative overflow-hidden">
                    <div className="relative z-10">
                        <div className="flex justify-between items-start mb-4">
                            <span className="material-symbols-outlined bg-white/20 p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>balance</span>
                            <span className="text-[10px] font-bold text-white/70 uppercase tracking-widest">Priority</span>
                        </div>
                        <p className="text-sm font-medium text-white/80 mb-1">Active Cases</p>
                        <h3 className="text-4xl font-extrabold">126</h3>
                        <p className="text-xs mt-4 text-white/60 font-medium">4 Cases require immediate filing before EOD.</p>
                    </div>
                    <div className="absolute -right-10 -bottom-10 opacity-10">
                        <span className="material-symbols-outlined text-[200px]" style={{ fontVariationSettings: "'wght' 200" }}>gavel</span>
                    </div>
                </div>

                {/* Main Content Column */}
                <div className="col-span-12 lg:col-span-8 space-y-6">
                    <div className="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden">
                        <div className="px-8 py-6 flex justify-between items-center border-b border-outline-variant/5">
                            <h3 className="text-lg font-bold flex items-center gap-2">
                                <span className="material-symbols-outlined text-primary">event_note</span>
                                Today's Hearing Schedule
                            </h3>
                            <button className="text-primary text-xs font-bold uppercase tracking-wider hover:underline">View Calendar</button>
                        </div>
                        <div className="divide-y divide-outline-variant/10">
                            <HearingRow time="09:30" period="AM" title="State vs. Miller & Sons" location="Superior Court - Courtroom 4B" type="Pre-Trial" />
                            <HearingRow time="11:15" period="AM" title="Acme Corp Merger Dispute" location="Federal District Court - Room 202" type="Evidentiary" />
                            <HearingRow time="02:45" period="PM" title="Estate of Julian Vance" location="Probate Court - Chambers" type="Arbitration" />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div className="bg-surface-container-lowest p-6 rounded-xl shadow-sm">
                            <h4 className="text-sm font-bold text-on-surface-variant mb-6 flex items-center gap-2">
                                <span className="material-symbols-outlined text-sm">trending_up</span>
                                Billable Hours Target
                            </h4>
                            <div className="flex items-end gap-3 mb-2">
                                {[65, 88, 40, 95, 15].map((h, i) => (
                                    <div key={i} className={`flex-1 ${i===4 ? 'h-28 border-2 border-dashed border-primary' : 'h-24'} bg-primary-container/30 rounded-lg relative overflow-hidden`}>
                                        <div className="absolute bottom-0 left-0 w-full bg-primary rounded-t-sm" style={{ height: `${h}%`, opacity: h < 30 ? 0.5 : 1 }}></div>
                                    </div>
                                ))}
                            </div>
                            <div className="flex justify-between text-[10px] font-bold text-on-surface-variant/50 uppercase">
                                <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span className="text-primary">Fri</span>
                            </div>
                        </div>
                        <div className="bg-surface-container-lowest p-6 rounded-xl shadow-sm flex flex-col justify-between">
                            <div>
                                <h4 className="text-sm font-bold text-on-surface-variant mb-2">Firm Load Balance</h4>
                                <p className="text-xs text-on-surface-variant leading-relaxed">System-wide bandwidth at <span className="text-primary font-bold">82%</span>. Redistribution recommended for 2 associates.</p>
                            </div>
                            <div className="mt-4">
                                <div className="flex items-center gap-2 mb-2">
                                    <div className="w-full bg-surface-container-low h-2 rounded-full overflow-hidden">
                                        <div className="bg-secondary w-[82%] h-full"></div>
                                    </div>
                                    <span className="text-[10px] font-bold">82%</span>
                                </div>
                                <button className="w-full py-2 bg-surface-container-high rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-outline-variant/20 transition-colors">Run Resource Audit</button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Sidebar Column */}
                <div className="col-span-12 lg:col-span-4 space-y-6">
                    <div className="bg-surface-container-high p-6 rounded-xl relative overflow-hidden">
                        <h4 className="text-xs font-bold uppercase tracking-widest text-on-surface-variant mb-6">Case Success Ratio</h4>
                        <div className="flex items-center justify-center py-4">
                            <div className="relative">
                                <svg className="w-32 h-32 transform -rotate-90">
                                    <circle className="text-surface-container-low" cx="64" cy="64" fill="transparent" r="56" stroke="currentColor" strokeWidth="8"></circle>
                                    <circle className="text-primary" cx="64" cy="64" fill="transparent" r="56" stroke="currentColor" strokeDasharray="351.8" strokeDashoffset="88" strokeWidth="8"></circle>
                                </svg>
                                <div className="absolute inset-0 flex flex-col items-center justify-center">
                                    <span className="text-2xl font-extrabold">75%</span>
                                    <span className="text-[8px] uppercase font-bold text-on-surface-variant">Settled</span>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-2 mt-4">
                            <div className="flex justify-between items-center text-xs">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                                    <span className="font-medium">Favorable Rulings</span>
                                </div>
                                <span className="font-bold">42</span>
                            </div>
                            <div className="flex justify-between items-center text-xs">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-secondary"></div>
                                    <span className="font-medium">In Mediation</span>
                                </div>
                                <span className="font-bold">18</span>
                            </div>
                        </div>
                    </div>

                    <div className="bg-surface-container-lowest p-6 rounded-xl shadow-sm">
                        <h4 className="text-sm font-bold text-on-surface mb-6">Associate Availability</h4>
                        <div className="space-y-4">
                            {[
                                { name: 'Marcus Holloway', status: 'In Hearing (until 12 PM)', color: 'bg-emerald-500', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBWUq3uAimxmXZnqj3YQAiOPX3lXJGnu-KmlqbJosajM0UpWg0Yy54cSDvxjHZIJj-m6-tuDXG4D_9N4_Ep3uohH0FVm5cyzeqF1XnalDG97ijydHuYsqHxCbhKXYOTriXKsT9a_sjcuLVKZj7sbgEZqd131d6vXOMI0ePSLOh4YFo4kG9WJ_zuNzuhplHdRTDe71G2nYvPPS189yCMAGp-azCOFO_50AIyfkVO6RcX6Kz1RhHUv8mH46H6rG92oQX_cIqB7lRXenhy' },
                                { name: 'Elena Vance', status: 'Reviewing Discovery', color: 'bg-amber-500', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBY9xtCeCLLELB4PTDKjRbOuhqeOsOKtzwtzEiCN8HQJnOe_EEUCasE_KX4tIlRAf9zIv58Kii75IhcdVmNCcquFqYZcL6K1s0WFAiuCpkOgHjJUbY2ouULOaWeuxwPNnR2O3U4gtqdxrX0dVkkmZsa7Wl6R9KqxciTbv4FsJ8wqfP7k08mTRqbTENQMWHdJScYcOnJ4WXi7aWtRSOru6c_9yD6dK803fkAFcLOznQd5Hyxhuni0h3ppUgn_lsn5oVzP2Rok4hEsD3G' },
                                { name: 'David Chen', status: 'Available', color: 'bg-emerald-500', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCmXU3NyleSqh6Og7ZgxaEDoImEbV1WU9qaBBip_HovnbqMpRgZeKWozvBqZZEXoPLz83BNKiGoSb0nhOCyLonPufrU3WAGMpzlzhfGE28tt4qbc-lWE6N_K5sB08lvyok5PWcgoxQtOd0blx3kZwoRgzB_iVp-SfDfijVemYOY2_1_reaqrbX4RK2wS_S41FYZidKWxUsh2aaSwtgzJ41PauNt6SWYY9ZLojxlRKM-cLl-yVmogw1y2A0ijSkZo_DAkM3X9C9VPDtP' }
                            ].map(member => (
                                <div key={member.name} className="flex items-center gap-3">
                                    <div className="relative">
                                        <img className="w-10 h-10 rounded-full object-cover" src={member.img} alt={member.name} />
                                        <div className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 ${member.color} border-2 border-white rounded-full`}></div>
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-xs font-bold">{member.name}</p>
                                        <p className="text-[10px] text-on-surface-variant">{member.status}</p>
                                    </div>
                                    <button className="text-primary"><span className="material-symbols-outlined text-lg">chat</span></button>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-6 py-2.5 bg-surface-container-low text-on-surface-variant rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-surface-container-high transition-colors">View All Staff</button>
                    </div>

                    <div className="bg-primary-container p-6 rounded-xl">
                        <div className="flex items-center gap-2 mb-4">
                            <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>campaign</span>
                            <h4 className="text-xs font-bold uppercase tracking-widest text-on-primary-container">Firm Update</h4>
                        </div>
                        <p className="text-sm font-bold text-on-primary-container mb-2 leading-tight">New Evidence Submission Standards</p>
                        <p className="text-xs text-on-primary-container/70 leading-relaxed mb-4">Please review the updated guidelines for digital evidence packaging for the Superior Court.</p>
                        <a className="inline-flex items-center text-xs font-bold text-primary group" href="#">
                            Read Memo 
                            <span className="material-symbols-outlined text-sm ml-1 group-hover:translate-x-1 transition-transform">arrow_forward</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
