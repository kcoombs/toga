from travertino.size import at_least
from rubicon.java import JavaClass
from ..libs.activity import MainActivity
from ..libs.android import R__attr
from ..libs.android.util import AttributeSet, Xml
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import (
    ProgressBar as A_ProgressBar,
    LinearLayout,
    LinearLayout__LayoutParams
)
from .base import Widget

class ProgressBar(Widget):
    def create(self):
        # progressBar = new ProgressBar(youractivity.this, null, android.R.attr.progressBarStyleLarge);
        # progressbar = A_ProgressBar(self._native_activity, attr_set, R__attr.progressBarStyleHorizontal)
        # progressbar = A_ProgressBar(self._native_activity, attr_set, R__attr.progressBarStyleLarge)
        # progressBar = A_ProgressBar(self._native_activity, None, R__attr.progressBarStyleLarge)
        # progressbar = A_ProgressBar(self._native_activity, attrs)

        # Constructor cons = ProgressBar.class.getConstructor(Context.class, AttributeSet.class, int.class);
        # ProgressBar progressbar = (ProgressBar) cons.newInstance(this, null, android.R.attr.progressBarStyleHorizontal);
        Context = JavaClass("android/content/Context")
        print('GET CLASS')
        clazz = A_ProgressBar(self._native_activity).getClass()
        print('GET CONSTRUCTOR')
        cons = clazz.getConstructor(Context, AttributeSet, int)  # not working
        constructors = clazz.getConstructors()  # not working
        print('INVOKING PROGRESSBAR')
        progressbar = cons.newInstance(self._native_activity, None, R__attr.progressBarStyleHorizontal)
        self.native = progressbar

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    @property
    def max(self):
        return self.interface.max

    def set_max(self, value):
        if value is not None:
            self.native.setMax(int(value))
        if self.interface.is_running:
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if self.max is None:
            self.native.setIndeterminate(True)
        else:
            self.native.setIndeterminate(False)

    def set_stopping_style(self):
        self.native.setIndeterminate(False)

    def set_value(self, value):
        if value is not None:
            self.native.setProgress(int(value))

    def rehint(self):
        # Android can crash when rendering some widgets until
        # they have their layout params set. Guard for that case.
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = at_least(self.native.getMeasuredHeight())
