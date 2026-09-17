
uint __thiscall FUN__text__0053f488(int param_1,char *param_2)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  char *pcVar4;
  uint local_8;
  
  iVar3 = 0;
  local_8 = 0;
  if ((param_2 == (char *)0x0) || (*param_2 == '\0')) {
    local_8 = 0xe40000;
  }
  else {
    uVar2 = 0x10;
    pcVar4 = param_2;
    do {
      cVar1 = *pcVar4;
      if (cVar1 != '\0') {
        if (cVar1 < 'x') {
          if ((cVar1 == 'w') || (cVar1 == 'a')) {
            iVar3 = 3;
          }
          else {
            if (cVar1 != 'b') {
              if (cVar1 == 'g') goto LAB__text__0053f514;
              if (cVar1 == 'r') goto LAB__text__0053f4ca;
              goto LAB__text__0053f4e0;
            }
LAB__text__0053f510:
            iVar3 = 2;
          }
        }
        else if (cVar1 == 'x') {
LAB__text__0053f4ca:
          iVar3 = 0;
        }
        else {
          if (cVar1 != 'y') {
            if (cVar1 == 'z') goto LAB__text__0053f510;
            goto LAB__text__0053f4e0;
          }
LAB__text__0053f514:
          iVar3 = 1;
        }
        pcVar4 = pcVar4 + 1;
      }
      local_8 = local_8 | iVar3 << ((byte)uVar2 & 0x1f);
      uVar2 = uVar2 + 2;
    } while (uVar2 < 0x18);
    if (*pcVar4 != '\0') {
LAB__text__0053f4e0:
      FUN__text__0053eb92(param_1,"invalid swizzle \'%s\'",param_2);
      *(undefined4 *)(param_1 + 0x98) = 1;
      local_8 = 0;
    }
  }
  return local_8;
}

