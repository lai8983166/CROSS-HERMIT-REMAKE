
/* WARNING: Restarted to delay deadcode elimination for space: stack */

void FUN__text__00585eb0(int param_1,_exception *param_2,ushort *param_3)

{
  int iVar1;
  undefined1 local_6c [40];
  undefined4 local_44;
  undefined4 local_40;
  uint local_34;
  uint local_14;
  uint *local_10;
  int local_c;
  int local_8;
  
  local_14 = (uint)*param_3;
  local_10 = &local_14;
  switch(param_2->type) {
  case 1:
  case 5:
    local_8 = 8;
    break;
  case 2:
    local_8 = 4;
    break;
  case 3:
    local_8 = 0x11;
    break;
  case 4:
    local_8 = 0x12;
    break;
  case 7:
    param_2->type = 1;
  default:
    local_8 = 0;
    break;
  case 8:
    local_8 = 0x10;
  }
  if ((local_8 != 0) && (iVar1 = FUN__text__0057e8c0(local_8,&param_2->retval,local_14), iVar1 == 0)
     ) {
    if ((param_1 == 0x10) || ((param_1 == 0x16 || (param_1 == 0x1d)))) {
      local_34 = local_34 & 0xffffffe1 | 3;
      local_44 = *(undefined4 *)&param_2->arg2;
      local_40 = *(undefined4 *)((int)&param_2->arg2 + 4);
    }
    else {
      local_34 = local_34 & 0xfffffffe;
    }
    FUN__text__0057e3f0(local_6c,local_10,local_8,param_1,&param_2->arg1,&param_2->retval);
  }
  FUN__text__0057f0d0(*local_10,0xffff);
  local_c = 0;
  if ((param_2->type != 8) && (DAT_00765150 == 0)) {
    local_c = __matherr(param_2);
  }
  if (local_c == 0) {
    FID_conflict___set_errno_from_matherr(param_2->type);
  }
  return;
}

