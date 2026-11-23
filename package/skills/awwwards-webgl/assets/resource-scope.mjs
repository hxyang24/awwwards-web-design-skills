/** Register only objects owned by this scene; do not traverse/dispose shared global assets. */
export class ResourceScope {
  #items = new Set();
  #disposed = false;
  add(resource) {
    if (this.#disposed) throw new Error('scope already disposed');
    if (!resource || typeof resource.dispose !== 'function') throw new TypeError('resource requires dispose()');
    this.#items.add(resource); return resource;
  }
  dispose() {
    if (this.#disposed) return;
    this.#disposed = true;
    const failures = [];
    [...this.#items].reverse().forEach((item) => { try { item.dispose(); } catch(e) { failures.push(e); } });
    this.#items.clear();
    if (failures.length) throw new AggregateError(failures, 'Some resources failed to dispose');
  }
  get isDisposed() { return this.#disposed; }
}
