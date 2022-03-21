using size_t = decltype(sizeof(0));

template <typename T, T... ts>
struct integer_sequence
{
    using value_type = T;
    static constexpr size_t size() { return sizeof...(ts); }
};
namespace detail
{
    // log(n) instantiation depth implementation of make_integer_sequence
    // something::integer_sequence is the injected class name of the nearest base
    // integer_sequence

    template <typename S1, typename S2>
    struct _merge;

    template <typename T, T... I1, T... I2>
    struct _merge<integer_sequence<T, I1...>, integer_sequence<T, I2...>>
        : integer_sequence<T, I1..., (sizeof...(I1) + I2)...>
    {
    };
    template <typename S1, typename S2>
    using _merge_t = typename _merge<S1, S2>::integer_sequence;

    template <typename T, size_t N>
    struct _generate;
    template <typename T, size_t N>
    using _generate_t = typename _generate<T, N>::integer_sequence;

    template <typename T, size_t N>
    struct _generate : _merge_t<_generate_t<T, N / 2>, _generate_t<T, N - N / 2>>
    {
    };

    template <typename T>
    struct _generate<T, 0> : integer_sequence<T>
    {
    };
    template <typename T>
    struct _generate<T, 1> : integer_sequence<T, 0>
    {
    };
}
template <typename T, size_t N>
using make_integer_sequence = detail::_generate_t<T, N>;
template <size_t... Is>
using index_sequence = integer_sequence<size_t, Is...>;
template <size_t N>
using make_index_sequence = make_integer_sequence<size_t, N>;
template <typename... Ts>
using index_sequence_for = make_index_sequence<sizeof...(Ts)>;