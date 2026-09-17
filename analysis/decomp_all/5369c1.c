
/* WARNING (jumptable): Unable to track spacebase fully for stack */

int * FUN__text__005369c1(void)

{
  int iVar1;
  int iVar2;
  int unaff_EBP;
  int *piVar3;
  
  FUN__text__0057158c();
  iVar1 = *(int *)(unaff_EBP + 8);
  iVar2 = *(int *)(iVar1 + 4);
  piVar3 = (int *)0x0;
  if (iVar2 < 0x31545845) {
    if (iVar2 == 0x31545844) {
      iVar2 = FUN__text__00428a40(0x10c4);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x20;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053682b(iVar1);
    }
    else if (iVar2 < 0x29) {
      if (iVar2 == 0x28) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0xd;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__00536058(iVar1);
      }
      else {
        switch(iVar2) {
        case 0x14:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 0;
          if (iVar2 == 0) {
LAB__text__005370b8:
            piVar3 = (int *)0x0;
          }
          else {
            piVar3 = (int *)FUN__text__0053549c(iVar1);
          }
          break;
        case 0x15:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 1;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__005355d1(iVar1);
          break;
        case 0x16:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 2;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__0053560e(iVar1);
          break;
        case 0x17:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 3;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__0053564b(iVar1);
          break;
        case 0x18:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 4;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535874(iVar1);
          break;
        case 0x19:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 5;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__005358b1(iVar1);
          break;
        case 0x1a:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 6;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535bbf(iVar1);
          break;
        case 0x1b:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 7;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535bfc(iVar1);
          break;
        case 0x1c:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 8;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535c39(iVar1);
          break;
        case 0x1d:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 9;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535c76(iVar1);
          break;
        case 0x1e:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 10;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535cb3(iVar1);
          break;
        case 0x1f:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 0xb;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535d7d(iVar1);
          break;
        default:
          goto switchD__text__00536a03_caseD_20;
        case 0x22:
          iVar2 = FUN__text__00428a40(0x106c);
          *(int *)(unaff_EBP + 8) = iVar2;
          *(undefined4 *)(unaff_EBP + -4) = 0xc;
          if (iVar2 == 0) goto LAB__text__005370b8;
          piVar3 = (int *)FUN__text__00535e29(iVar1);
        }
      }
    }
    else if (iVar2 < 0x3f) {
      if (iVar2 == 0x3e) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0x14;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__00536320(iVar1);
      }
      else if (iVar2 == 0x29) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0xe;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__00536095(iVar1);
      }
      else if (iVar2 == 0x32) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0xf;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__005360d2(iVar1);
      }
      else if (iVar2 == 0x33) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0x10;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__0053610f(iVar1);
      }
      else if (iVar2 == 0x34) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0x11;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__00536168(iVar1);
      }
      else if (iVar2 == 0x3c) {
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0x12;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__005362a6(iVar1);
      }
      else {
        if (iVar2 != 0x3d) goto switchD__text__00536a03_caseD_20;
        iVar2 = FUN__text__00428a40(0x106c);
        *(int *)(unaff_EBP + 8) = iVar2;
        *(undefined4 *)(unaff_EBP + -4) = 0x13;
        if (iVar2 == 0) goto LAB__text__005370b8;
        piVar3 = (int *)FUN__text__005362e3(iVar1);
      }
    }
    else if (iVar2 == 0x3f) {
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x15;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053635d(iVar1);
    }
    else if (iVar2 == 0x40) {
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x16;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053639a(iVar1);
    }
    else if (iVar2 == 0x41) {
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x17;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__005363d7(iVar1);
    }
    else if (iVar2 == 0x43) {
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x18;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__00536414(iVar1);
    }
    else {
      if (iVar2 != 0x46) goto switchD__text__00536a03_caseD_20;
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x19;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__00536451(iVar1);
    }
  }
  else if (iVar2 < 0x36314c21) {
    if (iVar2 == 0x36314c20) {
      iVar2 = FUN__text__00428a40(0x106c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x1a;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053648e(iVar1);
    }
    else if (iVar2 == 0x32545844) {
      iVar2 = FUN__text__00428a40(0x10c4);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x21;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__00536864(iVar1);
    }
    else if (iVar2 == 0x32595559) {
      iVar2 = FUN__text__00428a40(0x109c);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x1f;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__005369a9(iVar1);
    }
    else if (iVar2 == 0x33545844) {
      iVar2 = FUN__text__00428a40(0x10c4);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x22;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053689d(iVar1);
    }
    else if (iVar2 == 0x34545844) {
      iVar2 = FUN__text__00428a40(0x10c4);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x23;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__005368d6(iVar1);
    }
    else {
      if (iVar2 != 0x35545844) goto switchD__text__00536a03_caseD_20;
      iVar2 = FUN__text__00428a40(0x10c4);
      *(int *)(unaff_EBP + 8) = iVar2;
      *(undefined4 *)(unaff_EBP + -4) = 0x24;
      if (iVar2 == 0) goto LAB__text__005370b8;
      piVar3 = (int *)FUN__text__0053690f(iVar1);
    }
  }
  else if (iVar2 == 0x36314c41) {
    iVar2 = FUN__text__00428a40(0x106c);
    *(int *)(unaff_EBP + 8) = iVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0x1b;
    if (iVar2 == 0) goto LAB__text__005370b8;
    piVar3 = (int *)FUN__text__00536774(iVar1);
  }
  else if (iVar2 == 0x36315220) {
    iVar2 = FUN__text__00428a40(0x106c);
    *(int *)(unaff_EBP + 8) = iVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0x1c;
    if (iVar2 == 0) goto LAB__text__005370b8;
    piVar3 = (int *)FUN__text__005367b1(iVar1);
  }
  else if (iVar2 == 0x36315241) {
    iVar2 = FUN__text__00428a40(0x106c);
    *(int *)(unaff_EBP + 8) = iVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0x1d;
    if (iVar2 == 0) goto LAB__text__005370b8;
    piVar3 = (int *)FUN__text__005367ee(iVar1);
  }
  else {
    if (iVar2 != 0x59565955) goto switchD__text__00536a03_caseD_20;
    iVar2 = FUN__text__00428a40(0x109c);
    *(int *)(unaff_EBP + 8) = iVar2;
    *(undefined4 *)(unaff_EBP + -4) = 0x1e;
    if (iVar2 == 0) goto LAB__text__005370b8;
    piVar3 = (int *)FUN__text__00536991(iVar1);
  }
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  if ((piVar3 != (int *)0x0) && (piVar3[4] != 0)) {
    (**(code **)(*piVar3 + 0xc))();
  }
switchD__text__00536a03_caseD_20:
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return piVar3;
}

