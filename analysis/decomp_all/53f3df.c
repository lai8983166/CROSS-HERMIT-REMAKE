
uint __thiscall FUN__text__0053f3df(int param_1,char *param_2)

{
  char *pcVar1;
  uint uVar2;
  char cVar3;
  char *pcVar4;
  char *pcVar5;
  
  pcVar1 = param_2;
  uVar2 = 0;
  if ((param_2 == (char *)0x0) || (cVar3 = *param_2, pcVar5 = param_2, cVar3 == '\0')) {
    uVar2 = 0xf0000;
  }
  else {
    do {
      if (cVar3 < 'x') {
        if ((cVar3 == 'w') || (cVar3 == 'a')) {
          pcVar4 = (char *)0x3;
          uVar2 = uVar2 | 0x80000;
        }
        else {
          if (cVar3 != 'b') {
            if (cVar3 == 'g') goto LAB__text__0053f456;
            if (cVar3 != 'r') goto LAB__text__0053f460;
            goto LAB__text__0053f41b;
          }
LAB__text__0053f44c:
          pcVar4 = (char *)0x2;
          uVar2 = uVar2 | 0x40000;
        }
      }
      else if (cVar3 == 'x') {
LAB__text__0053f41b:
        pcVar4 = (char *)0x0;
        uVar2 = uVar2 | 0x10000;
      }
      else {
        if (cVar3 != 'y') {
          if (cVar3 != 'z') goto LAB__text__0053f460;
          goto LAB__text__0053f44c;
        }
LAB__text__0053f456:
        pcVar4 = (char *)0x1;
        uVar2 = uVar2 | 0x20000;
      }
      if ((pcVar5 != pcVar1) && (pcVar4 <= param_2)) {
LAB__text__0053f460:
        FUN__text__0053eb92(param_1,"invalid mask \'%s\'",pcVar1);
        *(undefined4 *)(param_1 + 0x98) = 1;
        return 0;
      }
      cVar3 = pcVar5[1];
      pcVar5 = pcVar5 + 1;
      param_2 = pcVar4;
    } while (cVar3 != '\0');
  }
  return uVar2;
}

