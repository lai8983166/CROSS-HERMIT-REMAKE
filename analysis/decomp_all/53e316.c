
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int __thiscall FUN__text__0053e316(int param_1,int param_2)

{
  float fVar1;
  undefined4 *puVar2;
  int iVar3;
  int *piVar4;
  undefined4 local_88;
  undefined4 local_84;
  undefined4 local_80;
  undefined4 local_7c;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  int local_24;
  int *local_20;
  undefined4 *local_1c;
  undefined4 *local_18;
  int *local_14;
  int *local_10;
  int *local_c;
  uint local_8;
  
  local_24 = *(int *)(param_1 + 0x460);
  if ((*(int *)(local_24 * 0xd0 + 0x50 + param_1) != 0) ||
     (iVar3 = FUN__text__0053d35b(), -1 < iVar3)) {
    local_10 = (int *)(param_1 + 0x48c);
    if ((*local_10 == 0) || (*(int *)(param_1 + 0x490) == 0)) {
      local_8 = 0;
      do {
        (**(code **)(**(int **)(param_1 + 8) + 0xd0))(*(int **)(param_1 + 8));
        (**(code **)(**(int **)(param_1 + 8) + 0x130))(*(int **)(param_1 + 8),0x142);
        (**(code **)(**(int **)(param_1 + 8) + 0x160))(*(int **)(param_1 + 8),0);
        (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x474);
        local_1c = *(undefined4 **)(param_1 + 0xc);
        fVar1 = (float)(int)local_1c;
        if ((int)local_1c < 0) {
          fVar1 = fVar1 + _DAT_005d0a44;
        }
        fVar1 = _DAT_005d0a40 / fVar1;
        FUN__text__005397c3(&local_88,fVar1 - _DAT_005d0a40,fVar1 + _DAT_005d0a40,
                            _DAT_005d0a5c - fVar1,1.0 - fVar1,0,_DAT_005d0e20);
        (**(code **)(**(int **)(param_1 + 8) + 0x94))(*(int **)(param_1 + 8),3,&local_88);
        local_48 = 0;
        local_44 = 0x3f800000;
        local_40 = 0;
        local_30 = 0;
        local_2c = 0;
        local_28 = 0;
        local_3c = 0;
        local_38 = 0;
        local_34 = 0x3f800000;
        FUN__text__00538f7c(&local_88,&local_3c,&local_30,&local_48);
        (**(code **)(**(int **)(param_1 + 8) + 0x94))(*(int **)(param_1 + 8),2,&local_88);
        local_50 = 0;
        local_54 = 0;
        local_58 = 0;
        local_5c = 0;
        local_64 = 0;
        local_68 = 0;
        local_6c = 0;
        local_70 = 0;
        local_78 = 0;
        local_7c = 0;
        local_80 = 0;
        local_84 = 0;
        local_4c = 0x3f800000;
        local_60 = 0x3f800000;
        local_74 = 0x3f800000;
        local_88 = 0x3f800000;
        (**(code **)(**(int **)(param_1 + 8) + 0x94))(*(int **)(param_1 + 8),0x100,&local_88);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),7,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),8,3);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x16,1);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x80,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x88,1);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x97,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x98,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0xa4,1);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0xa7,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x1b,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x1c,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x1d,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x34,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x89,0);
        (**(code **)(**(int **)(param_1 + 8) + 200))(*(int **)(param_1 + 8),0x91,1);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,1,4);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,2,2);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,3,0);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,4,4);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,5,2);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,6,0);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),1,1,1);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),1,4,1);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0x10,2);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0x11,2);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0x12,2);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0xb,0);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0xd,3);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0xe,3);
        (**(code **)(**(int **)(param_1 + 8) + 0xfc))(*(int **)(param_1 + 8),0,0x18,0);
        if (local_8 == 0) {
          (**(code **)(**(int **)(param_1 + 8) + 0xf4))(*(int **)(param_1 + 8),0,0);
          (**(code **)(**(int **)(param_1 + 8) + 0x14c))(*(int **)(param_1 + 8),0,0,0);
          (**(code **)(**(int **)(param_1 + 8) + 0x154))(*(int **)(param_1 + 8),0,0);
          piVar4 = local_10;
        }
        else {
          piVar4 = (int *)(param_1 + 0x490);
        }
        (**(code **)(**(int **)(param_1 + 8) + 0xd4))(*(int **)(param_1 + 8),piVar4);
        local_8 = local_8 + 1;
      } while (local_8 < 2);
    }
    (**(code **)(**(int **)(param_1 + 8) + 0xdc))(*(int **)(param_1 + 8),*local_10);
    (**(code **)(**(int **)(param_1 + 8) + 0xd8))
              (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0x490));
    local_20 = (int *)(param_1 + 0x38);
    local_8 = 0;
    do {
      local_14 = (int *)*local_20;
      if (local_14 != (int *)0x0) {
        local_1c = (undefined4 *)((local_8 + local_24 * 2) * 0x68 + 0x50 + param_1);
        local_18 = local_1c + param_2 * 4 + 2;
        if (local_18[3] != 0) {
          if (local_20[4] == 0) {
            local_14 = local_20 + 2;
            if ((*local_14 == 0) &&
               (iVar3 = (**(code **)(**(int **)(param_1 + 8) + 100))
                                  (*(int **)(param_1 + 8),*(undefined4 *)(param_1 + 0xc),
                                   *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x10),0,
                                   1,local_14), iVar3 < 0)) goto LAB__text__0053e886;
            (**(code **)(**(int **)(param_1 + 8) + 0x7c))(*(int **)(param_1 + 8),*local_14,0);
          }
          else {
            (**(code **)(*local_14 + 0x3c))(local_14,0,&local_c);
            (**(code **)(**(int **)(param_1 + 8) + 0x7c))(*(int **)(param_1 + 8),local_c,0);
            if (local_c != (int *)0x0) {
              (**(code **)(*local_c + 8))(local_c);
              local_c = (int *)0x0;
            }
          }
          (**(code **)(**(int **)(param_1 + 8) + 0xa0))(*(int **)(param_1 + 8),param_1 + 0x474);
          puVar2 = local_1c;
          (**(code **)(**(int **)(param_1 + 8) + 0x14c))(*(int **)(param_1 + 8),0,*local_1c,0x18);
          (**(code **)(**(int **)(param_1 + 8) + 0x154))(*(int **)(param_1 + 8),puVar2[1],0);
          (**(code **)(**(int **)(param_1 + 8) + 0xf4))
                    (*(int **)(param_1 + 8),0,*(undefined4 *)(param_1 + 0x30));
          (**(code **)(**(int **)(param_1 + 8) + 0x88))(*(int **)(param_1 + 8));
          (**(code **)(**(int **)(param_1 + 8) + 0x11c))
                    (*(undefined4 *)(param_1 + 8),4,*local_18,local_18[1],local_18[2],
                     (uint)local_18[3] / 3);
          (**(code **)(**(int **)(param_1 + 8) + 0x8c))(*(int **)(param_1 + 8));
        }
      }
      local_8 = local_8 + 1;
      local_20 = local_20 + 1;
    } while (local_8 < 2);
    iVar3 = 0;
LAB__text__0053e886:
    (**(code **)(**(int **)(param_1 + 8) + 0xd8))(*(int **)(param_1 + 8),*local_10);
  }
  return iVar3;
}

