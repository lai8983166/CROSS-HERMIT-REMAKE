
undefined4 FUN__text__00584030(int param_1)

{
  code *pcVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  
  FUN__text__00577040(1);
  if (param_1 == 0) {
    puVar2 = &DAT_0080a68c;
    uVar3 = 2;
    pcVar1 = DAT_0080a68c;
  }
  else {
    puVar2 = &DAT_0080a690;
    uVar3 = 0x15;
    pcVar1 = DAT_0080a690;
  }
  if (pcVar1 == (code *)0x0) {
    FUN__text__005770e0(1);
    uVar3 = 0;
  }
  else {
    if (pcVar1 == (code *)0x1) {
      FUN__text__005770e0(1,1,puVar2,uVar3);
    }
    else {
      *puVar2 = 0;
      FUN__text__005770e0(1,pcVar1,puVar2,uVar3);
      (*pcVar1)(uVar3);
    }
    uVar3 = 1;
  }
  return uVar3;
}

