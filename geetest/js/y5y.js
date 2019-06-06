f800.y5Y = function () {
    return {
        k5Y: function g5Y(G5Y=39, o5Y=12) {
            var T5Y = 2;
            while (T5Y !== 10) {
                switch (T5Y) {
                    case 12:
                        a5Y += 1;
                        T5Y = 8;
                        break;
                    case 2:
                        var H5Y = [];
                        T5Y = 1;
                        break;
                    case 4:
                        H5Y[(b5Y + o5Y) % G5Y] = [];
                        T5Y = 3;
                        break;
                    case 6:
                        T5Y = t5Y >= 0 ? 14 : 12;
                        break;
                    case 13:
                        t5Y -= 1;
                        T5Y = 6;
                        break;
                    case 14:
                        H5Y[a5Y][(t5Y + o5Y * a5Y) % G5Y] = H5Y[t5Y];
                        T5Y = 13;
                        break;
                    case 1:
                        var b5Y = 0;
                        T5Y = 5;
                        break;
                    case 11:
                        return H5Y;
                        break;
                    case 9:
                        var a5Y = 0;
                        T5Y = 8;
                        break;
                    case 5:
                        T5Y = b5Y < G5Y ? 4 : 9;
                        break;
                    case 7:
                        var t5Y = G5Y - 1;
                        T5Y = 6;
                        break;
                    case 3:
                        b5Y += 1;
                        T5Y = 5;
                        break;
                    case 8:
                        T5Y = a5Y < G5Y ? 7 : 11;
                        break;
                }
            }
        }(39, 12)
    };
}();

