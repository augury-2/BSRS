import SwiftUI

/// Rules-based insights + an optional AI chat. Works offline (rules engine);
/// richer answers when online.
struct CoachView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var snapshot: WeeklySnapshot?
    @State private var insights: [CoachingInsight] = []
    @State private var messages: [ChatMessage] = []
    @State private var draft = ""
    @State private var sending = false

    var body: some View {
        VStack(spacing: 0) {
            ScrollViewReader { proxy in
                ScrollView {
                    VStack(alignment: .leading, spacing: 14) {
                        Card {
                            VStack(alignment: .leading, spacing: 8) {
                                HStack { Text("This week's insights").font(.headline); Spacer()
                                    ConnectivityPill(isOnline: env.coach.isOnline) }
                                ForEach(insights) { InsightCard(insight: $0, expanded: true) }
                            }
                        }
                        ForEach(messages) { msg in ChatBubble(message: msg).id(msg.id) }
                        if sending { ProgressView().padding(.leading) }
                    }.padding()
                }
                .onChange(of: messages.count) { _, _ in
                    if let last = messages.last { withAnimation { proxy.scrollTo(last.id, anchor: .bottom) } }
                }
            }
            suggestionChips
            inputBar
        }
        .navigationTitle("Coach")
        .navigationBarTitleDisplayMode(.inline)
        .task {
            guard let p = env.store.currentProfile() else { return }
            let snap = SnapshotBuilder.build(store: env.store, profile: p)
            snapshot = snap
            insights = CoachingEngine.analyze(snap)
        }
    }

    private var suggestionChips: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack {
                ForEach(["Why am I not losing weight?", "How much protein?", "Add more fiber?", "Is my pace okay?"], id: \.self) { q in
                    Button(q) { draft = q; send() }
                        .font(.caption).padding(.horizontal, 12).padding(.vertical, 7)
                        .background(Theme.accent.opacity(0.15), in: Capsule())
                }
            }.padding(.horizontal)
        }.frame(height: 44)
    }

    private var inputBar: some View {
        HStack {
            TextField("Ask your coach…", text: $draft, axis: .vertical)
                .textFieldStyle(.roundedBorder)
            Button { send() } label: { Image(systemName: "arrow.up.circle.fill").font(.title2) }
                .disabled(draft.trimmingCharacters(in: .whitespaces).isEmpty || sending)
        }.padding()
    }

    private func send() {
        let q = draft.trimmingCharacters(in: .whitespaces)
        guard !q.isEmpty, let snap = snapshot else { return }
        messages.append(ChatMessage(role: .user, content: q))
        draft = ""; sending = true
        Task {
            let reply = await env.coach.ask(q, history: messages, snapshot: snap)
            messages.append(reply)
            sending = false
        }
    }
}

struct ChatBubble: View {
    var message: ChatMessage
    var body: some View {
        HStack {
            if message.role == .user { Spacer() }
            Text(message.content)
                .padding(12)
                .background(message.role == .user ? Theme.accent.opacity(0.20) : Color.secondary.opacity(0.12),
                            in: RoundedRectangle(cornerRadius: 14))
                .frame(maxWidth: 300, alignment: message.role == .user ? .trailing : .leading)
            if message.role != .user { Spacer() }
        }
    }
}

#Preview { NavigationStack { CoachView() }.environment(AppEnvironment.preview()) }
