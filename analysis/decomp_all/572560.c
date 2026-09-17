
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int FUN__text__00572560(int param_1,uint param_2)

{
  int iVar1;
  
  if ((param_2._2_2_ & 0x7ff0) == 0x7ff0) {
    iVar1 = FUN__text__0057eed0(param_1,param_2);
    if (iVar1 == 1) {
      iVar1 = 0x200;
    }
    else if (iVar1 == 2) {
      iVar1 = 4;
    }
    else if (iVar1 == 3) {
      iVar1 = 2;
    }
    else {
      iVar1 = 1;
    }
  }
  else if (((param_2 & 0x7ff00000) == 0) && (((param_2 & 0xfffff) != 0 || (param_1 != 0)))) {
    iVar1 = (-(uint)((param_2 & 0x80000000) != 0) & 0xffffff90) + 0x80;
  }
  else if ((double)CONCAT26(param_2._2_2_,CONCAT24((undefined2)param_2,param_1)) == _DAT_00592d98) {
    iVar1 = (-(uint)((param_2 & 0x80000000) != 0) & 0xffffffe0) + 0x40;
  }
  else {
    iVar1 = (-(uint)((param_2 & 0x80000000) != 0) & 0xffffff08) + 0x100;
  }
  return iVar1;
}

