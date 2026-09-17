
int __thiscall FUN__text__0046c480(int param_1,int param_2,uint param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_6c [26];
  
  puVar2 = local_6c;
  for (iVar1 = 0x1a; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch((&DAT_006c2de0)[(param_3 & 0xffff) * 0x48]) {
  case 1:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
    case 2:
    case 3:
    case 4:
      return param_4;
    case 5:
    case 6:
    case 7:
    case 100:
      return 0x6e;
    default:
    }
    break;
  case 2:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
    case 3:
    case 5:
    case 6:
    case 7:
    case 100:
      return 0x6e;
    case 2:
    case 4:
      return param_4;
    default:
    }
    break;
  case 3:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
    case 3:
      return param_4;
    case 2:
    case 4:
    case 5:
    case 6:
    case 7:
    case 100:
      return 0x6e;
    default:
    }
    break;
  case 4:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 100:
      return 100;
    default:
    }
    break;
  case 5:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 100:
      return 0x6e;
    default:
    }
    break;
  case 6:
    switch(param_4) {
    case 0:
      return 0;
    case 1:
      if (*(short *)(param_2 + 2) == *(short *)(param_1 + 0x30992)) {
        return param_4;
      }
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 100:
      return 0x6e;
    }
    break;
  default:
    if (-1 < param_4) {
      if (param_4 < 8) {
        return 0;
      }
      if (param_4 == 100) {
        return 0x6e;
      }
    }
  }
  return 0;
}

